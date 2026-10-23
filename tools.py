import os
import requests
import yfinance as yf
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a given city.
    
    Args:
        location: The city name (e.g., 'London', 'New York').
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY environment variable not set."
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            return f"Error: Could not find weather for '{location}'. {data.get('message', '')}"
        
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        return f"The weather in {location} is {temp}°C with {desc}. Humidity is {humidity}%."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


@tool
def get_stock_price(symbol: str) -> str:
    """Get the current stock price for a given ticker symbol.
    
    Args:
        symbol: The stock ticker symbol (e.g., 'AAPL', 'GOOGL', 'TSLA').
    """
    try:
        ticker = yf.Ticker(symbol.upper())
        hist = ticker.history(period="1d")
        
        if hist.empty:
            return f"Error: No data found for symbol '{symbol}'. Please check the ticker."
        
        current_price = hist['Close'].iloc[-1]
        info = ticker.info
        prev_close = info.get('previousClose', current_price)
        change = current_price - prev_close
        pct_change = (change / prev_close) * 100 if prev_close else 0
        
        return (f"The current price of {symbol.upper()} is ${current_price:.2f}. "
                f"Change: {change:+.2f} ({pct_change:+.2f}%)")
    except Exception as e:
        return f"Error fetching stock data: {str(e)}"