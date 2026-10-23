"""Plain Python functions the chatbot can call. No LLM code lives here."""
from __future__ import annotations

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 10

WEATHER_CODES = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "rime fog", 51: "light drizzle", 53: "drizzle",
    55: "heavy drizzle", 61: "light rain", 63: "rain", 65: "heavy rain",
    71: "light snow", 73: "snow", 75: "heavy snow", 80: "rain showers",
    81: "heavy rain showers", 82: "violent rain showers", 95: "thunderstorm",
    96: "thunderstorm with hail", 99: "severe thunderstorm with hail",
}


def get_weather(city: str, units: str = "celsius") -> dict:
    """Current weather for a city via Open-Meteo (free, no API key)."""
    try:
        geo = requests.get(
            GEOCODE_URL, params={"name": city, "count": 1}, timeout=TIMEOUT
        ).json()
        if not geo.get("results"):
            return {"error": f"Could not find a city named '{city}'."}
        place = geo["results"][0]

        data = requests.get(
            FORECAST_URL,
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,apparent_temperature,relative_humidity_2m,"
                           "wind_speed_10m,weather_code",
                "temperature_unit": units,
            },
            timeout=TIMEOUT,
        ).json()["current"]

        return {
            "city": place["name"],
            "country": place.get("country"),
            "temperature": data["temperature_2m"],
            "feels_like": data["apparent_temperature"],
            "unit": "°C" if units == "celsius" else "°F",
            "humidity_pct": data["relative_humidity_2m"],
            "wind_kmh": data["wind_speed_10m"],
            "conditions": WEATHER_CODES.get(data["weather_code"], "unknown"),
        }
    except Exception as exc:  # network / parsing problems become tool output, not crashes
        return {"error": f"Weather lookup failed: {exc}"}


def get_stock_price(symbol: str) -> dict:
    """Latest price and daily change for a ticker via yfinance."""
    try:
        import yfinance as yf

        info = yf.Ticker(symbol.upper()).fast_info
        price = float(info["last_price"])
        prev = float(info["previous_close"])
        return {
            "symbol": symbol.upper(),
            "price": round(price, 2),
            "currency": info.get("currency", "USD"),
            "previous_close": round(prev, 2),
            "change_pct": round((price - prev) / prev * 100, 2),
        }
    except Exception as exc:
        return {"error": f"Could not fetch '{symbol}': {exc}"}


def calculate_stock_value(symbol: str, shares: float) -> dict:
    """Total market value of a position: latest price x number of shares."""
    quote = get_stock_price(symbol)
    if "error" in quote:
        return quote
    return {
        "symbol": quote["symbol"],
        "shares": shares,
        "price": quote["price"],
        "currency": quote["currency"],
        "total_value": round(quote["price"] * shares, 2),
    }
