"""Tool registry: one definition feeds both the OpenAI router and the LangChain agent."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable, Literal

from pydantic import BaseModel, Field, ValidationError

from app import tools


class WeatherInput(BaseModel):
    city: str = Field(..., description="City name, e.g. 'Hyderabad' or 'Paris'.")
    units: Literal["celsius", "fahrenheit"] = Field(
        "celsius", description="Temperature unit."
    )


class StockPriceInput(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol, e.g. 'AAPL', 'TSLA'.")


class StockValueInput(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol, e.g. 'MSFT'.")
    shares: float = Field(..., gt=0, description="Number of shares held.")


@dataclass(frozen=True)
class ToolSpec:
    fn: Callable
    input_model: type[BaseModel]
    description: str


TOOLS: dict[str, ToolSpec] = {
    "get_weather": ToolSpec(
        tools.get_weather, WeatherInput,
        "Get the current weather for a city. Use for any weather or temperature question.",
    ),
    "get_stock_price": ToolSpec(
        tools.get_stock_price, StockPriceInput,
        "Get the latest price and daily percent change for a stock ticker.",
    ),
    "calculate_stock_value": ToolSpec(
        tools.calculate_stock_value, StockValueInput,
        "Calculate the total value of N shares of a stock at the latest price.",
    ),
}


def openai_tools() -> list[dict]:
    """Tool definitions in OpenAI function-calling format."""
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": spec.description,
                "parameters": spec.input_model.model_json_schema(),
            },
        }
        for name, spec in TOOLS.items()
    ]


def dispatch(name: str, arguments_json: str) -> str:
    """Validate the model's arguments and run the matching Python function.

    Always returns a JSON string so errors flow back to the model instead of crashing.
    """
    spec = TOOLS.get(name)
    if spec is None:
        return json.dumps({"error": f"Unknown tool '{name}'."})
    try:
        args = spec.input_model.model_validate_json(arguments_json or "{}")
    except ValidationError as exc:
        return json.dumps({"error": f"Invalid arguments: {exc.errors()[0]['msg']}"})
    return json.dumps(spec.fn(**args.model_dump()))
