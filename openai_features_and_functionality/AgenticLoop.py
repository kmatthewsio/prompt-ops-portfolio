from openai import OpenAI
import os
from dotenv import load_dotenv
from venv import create

MODEL = "gpt-4.1-mini"

load_dotenv()  # Load environment variables from .env file

# Create an OpenAI client instance
client = OpenAI(
    # Replace with your actual API key or use: api_key=os.environ.get("OPENAI_API_KEY")
    api_key= os.getenv("OPENAI_API_KEY")
)

def ask_ai(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages= [
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content

# The simplest agentic loop: Think -> Act -> Repeat
def simple_agent(user_input):
    for step in range(3): # Just 3 steps to keep it simple# Just 3 steps to keep it simple
        print(f"Step { step + 1}:")

        # THINK: Ask AI what to do next
        thinking = ask_ai(f"I need help with: '{user_input}', What should I do next?")
        print (f" Thinking: {thinking}")

        # ACT: Ask AI to do it
        action = ask_ai(f"Now do this: {thinking}")
        print(f" Action: {action}")

        # REPEAT: Continue to next step
        print()

simple_agent("Help me understand Python loops")