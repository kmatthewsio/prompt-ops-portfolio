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

def ask_with_role(role, question):
    """Give the AI a role and ask a question"""

    messages = [
        {
            "role": "system",
            "content": f"You are { role }"
        },
        {
            "role": "user", "content": question
        }
    ]

    responses = client.chat.completions.create(model=MODEL,messages=messages,max_tokens=200)

    return responses.choices[0].message.content

question = "How should I invest, $10,000?"

advisor_answer = ask_with_role("a conservative financial advisor", question)
print(f"Financial Advisor: { advisor_answer}")
print()

crypto_answer = ask_with_role("an enthusiastic crypto investor", question)
print(f"Crypto Enthusiast: { crypto_answer}")
print()

grandma_answer = ask_with_role(" a wise grandmother who lived through the great depression", question)
print(f"Grandmother: { grandma_answer}")
print()