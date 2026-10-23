"""Backend 2: the same tools exposed through a LangChain agent."""
from __future__ import annotations

import json
import os

from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI

from app.registry import TOOLS
from app.openai_router import SYSTEM_PROMPT


def build_tools() -> list[StructuredTool]:
    def wrap(fn):
        # LangChain tools should return strings
        return lambda **kwargs: json.dumps(fn(**kwargs))

    return [
        StructuredTool.from_function(
            func=wrap(spec.fn),
            name=name,
            description=spec.description,
            args_schema=spec.input_model,
        )
        for name, spec in TOOLS.items()
    ]


class LangChainAgent:
    def __init__(self, model: str | None = None):
        llm = ChatOpenAI(model=model or os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
        self.agent = create_agent(llm, build_tools(), system_prompt=SYSTEM_PROMPT)
        self.history: list = []

    def chat(self, user_text: str) -> str:
        self.history.append({"role": "user", "content": user_text})
        seen = len(self.history)
        result = self.agent.invoke({"messages": self.history})
        self.history = result["messages"]  # keep tool calls + replies as memory
        for m in result["messages"][seen:]:  # log only this turn's routing
            for call in getattr(m, "tool_calls", None) or []:
                print(f"  [route] {call['name']}({call['args']})")
        return result["messages"][-1].content
