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

# Construct a conversation history manually for a knock-knock joke
history = [
    {"role": "user", "content": "tell me a joke."}
]

# Create a response using the conversation history
response = client.responses.create(
    model=MODEL,
    input="tell me a joke"
    #store=False #we are not storing the conversation automatically
)

print("Joke", response.output_text)

#history += [{"role": el.role, "content": el.content} for el in response.output]

#history.append({"role": "user", "content": "tell me another"})

second_response = client.responses.create(
    model=MODEL,
    previous_response_id=response.id,
    input=[{"role": "user", "content": "explain why this is funny."}]
)

print("Explanation:", second_response.output_text)
