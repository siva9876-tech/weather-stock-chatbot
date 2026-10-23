# 🤖 Weather & Stock Chatbot

A command-line AI assistant built with [LangChain](https://www.langchain.com/) that answers questions about **current weather** and **live stock prices**. It uses OpenAI's `gpt-4o-mini` model with tool calling to decide when to fetch real-time data from the OpenWeatherMap API and Yahoo Finance.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Tools Reference](#tools-reference)
- [Troubleshooting](#troubleshooting)
- [Dependencies](#dependencies)

---

## Features

- 💬 Interactive chat loop in the terminal
- 🌤️ Current weather lookup for any city (temperature, conditions, humidity)
- 📈 Live stock price lookup with daily change and percentage change
- 🧠 Automatic tool selection: the LLM decides which tool to call based on your question
- 🔐 API keys loaded from a `.env` file, never hard-coded
- 🛡️ Graceful error messages for missing keys, invalid cities, and bad tickers

---

## How It Works

1. You type a question, such as *"What's the weather in Paris?"* or *"How is TSLA doing?"*
2. The agent (created with `langchain.agents.create_agent`) sends your message to `gpt-4o-mini`.
3. The model decides whether to call `get_weather`, `get_stock_price`, or answer directly.
4. The selected tool runs, calling OpenWeatherMap or Yahoo Finance and returning a result string.
5. The model turns the tool output into a natural-language reply, which is printed in the terminal.

```
You ──► Agent (gpt-4o-mini) ──► Tool call ──► OpenWeatherMap / yfinance
                ▲                                      │
                └────────────── tool result ◄──────────┘
                │
                ▼
              Reply
```

---

## Project Structure

```
.
├── main.py            # Entry point: builds the agent and runs the chat loop
├── tools.py           # Tool definitions: get_weather and get_stock_price
├── requirements.txt   # Python dependencies
├── .env               # Your API keys (you create this; do not commit it)
└── README.md
```



## Installation

1. **Clone or download** the project, then move into its folder:

   ```bash
   cd <project-folder>
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   # macOS / Linux
   python -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Create a file named `.env` in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENWEATHER_API_KEY=your_openweathermap_api_key_here
```

---

## Usage

Start the chatbot:

```bash
python main.py
```

You'll see:

```
🤖 Chatbot ready! Ask about weather or stocks (type 'quit' to exit).

You:
```

Type `quit` or `exit` to leave.

### Example session

```
You: What's the weather like in London?
Bot: The weather in London is 14.2°C with light rain. Humidity is 82%.

You: What's the price of AAPL?
Bot: The current price of AAPL is $189.45. Change: +1.20 (+0.64%)

You: Should I carry an umbrella in Tokyo, and how is GOOGL doing?
Bot: (calls both tools and combines the results in one reply)
```

> Actual values will differ; they reflect live data at the time you ask.





## Troubleshooting

| Problem | Likely cause and fix |
| ------- | -------------------- |
| `ValueError: Please set OPENAI_API_KEY in your .env file.` | The `.env` file is missing, misnamed, or not in the directory you run `python main.py` from. |
| `ImportError: cannot import name 'create_agent'` | Your LangChain version is too old. Run `pip install -U "langchain>=1.0"`. |
| Weather tool says `Invalid API key` | Key is wrong or not yet activated. New OpenWeatherMap keys can take time to become active. |
| `Could not find weather for '<city>'` | Check the spelling or try `"City,CountryCode"` (e.g., `"Paris,FR"`). |
| Stock tool returns "No data found" | Verify the ticker. Non-US exchanges often need a suffix (e.g., `RELIANCE.NS`, `TCS.BO`). |
| Stock data errors or rate limiting | Yahoo Finance is an unofficial source and can throttle requests. Wait a moment, or upgrade with `pip install -U yfinance`. |


## Dependencies

From `requirements.txt`:

| Package            | Purpose                                   |
| ------------------ | ----------------------------------------- |
| `openai`           | OpenAI API client                         |
| `langchain`        | Agent framework (`create_agent`)          |
| `langchain-openai` | OpenAI model integration for LangChain    |
| `pydantic`         | Data validation used by LangChain         |
| `requests`         | HTTP calls to OpenWeatherMap              |
| `yfinance`         | Stock market data from Yahoo Finance      |
| `python-dotenv`    | Loads environment variables from `.env`   |
| `pytest`           | Testing framework (for adding tests)      |

---

## Author

Name : SIVA SHANKAR MAMIDISETTI
Ph.No : 7330712258
Email : sivamamidietti98765@gmail.com
[LinkedIN](https://www.linkedin.com/in/siva-shankar-mamidisetti)

