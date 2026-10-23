"""Backend 1: intent routing with raw OpenAI function calling."""
from __future__ import annotations

import os

from openai import OpenAI

from app.registry import dispatch, openai_tools

SYSTEM_PROMPT = (
    "You are a helpful assistant that can check the weather and look up or calculate "
    "stock prices. Use the provided tools for those requests; never guess live data. "
    "If a required detail is missing (e.g. which city), ask the user. "
    "For anything else, answer briefly from general knowledge."
)


class OpenAIRouter:
    def __init__(self, model: str | None = None):
        self.client = OpenAI()  # reads OPENAI_API_KEY
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

    def chat(self, user_text: str, max_steps: int = 5) -> str:
        self.messages.append({"role": "user", "content": user_text})

        for _ in range(max_steps):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=openai_tools(),
                tool_choice="auto",  # the model decides: answer directly or route to a tool
            )
            message = response.choices[0].message
            self.messages.append(message.model_dump(exclude_none=True))

            if not message.tool_calls:  # no more routing needed -> final answer
                return message.content or ""

            # The model may request several tools at once (e.g. weather in 2 cities).
            for call in message.tool_calls:
                print(f"  [route] {call.function.name}({call.function.arguments})")
                result = dispatch(call.function.name, call.function.arguments)
                self.messages.append(
                    {"role": "tool", "tool_call_id": call.id, "content": result}
                )

        return "Sorry, I couldn't complete that request."
