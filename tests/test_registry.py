"""Offline tests: no network or API key needed."""
import json

from app import registry, tools


def test_openai_schemas_cover_all_tools():
    names = {t["function"]["name"] for t in registry.openai_tools()}
    assert names == {"get_weather", "get_stock_price", "calculate_stock_value"}


def test_dispatch_unknown_tool():
    out = json.loads(registry.dispatch("nope", "{}"))
    assert "error" in out


def test_dispatch_rejects_bad_arguments():
    out = json.loads(registry.dispatch("calculate_stock_value", '{"symbol": "AAPL", "shares": -5}'))
    assert "error" in out


def test_dispatch_routes_to_function(monkeypatch):
    monkeypatch.setattr(
        tools, "get_stock_price",
        lambda symbol: {"symbol": symbol, "price": 100.0, "currency": "USD",
                        "previous_close": 99.0, "change_pct": 1.01},
    )
    out = json.loads(registry.dispatch("calculate_stock_value", '{"symbol": "AAPL", "shares": 3}'))
    assert out["total_value"] == 300.0
