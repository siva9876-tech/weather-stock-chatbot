import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from tools import get_weather, get_stock_price

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Please set OPENAI_API_KEY in your .env file.")

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather, get_stock_price],
    system_prompt="You are a helpful financial and weather assistant."
)

def chat():
    print("🤖 Chatbot ready! Ask about weather or stocks (type 'quit' to exit).")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            break
        
        result = agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        
        final_message = result["messages"][-1].content
        print(f"Bot: {final_message}")

if __name__ == "__main__":
    chat()