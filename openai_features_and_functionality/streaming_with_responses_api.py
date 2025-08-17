from openai import OpenAI
import os
from dotenv import load_dotenv
from venv import create
from statistics import mode

#Streaming Enabled: By setting stream=True in the API request, we stream the model's output incrementally.
#Event Handling: The code loops over each event, printing its type and any text deltas as they are generated.
#Example Prompt: We used a tongue twister prompt as a different example to show that you can stream various types of outputs.

MODEL = "gpt-4.1-mini"

load_dotenv()  # Load environment variables from .env file

# Create an OpenAI client instance
client = OpenAI(
    # Replace with your actual API key or use: api_key=os.environ.get("OPENAI_API_KEY")
    api_key= os.getenv("OPENAI_API_KEY")
)

stream = client.responses.create (
    model=MODEL,
    input = [
        {"role": "user", "content": "Recite 'Peter Piper picked a peck of pickled peppers' five times in a row"}
    ],
    stream=True
    )


# Iterate over streaming events and print details
# for event in stream:
#     # Depending on the event type, you can handle it accordingly
#     if hasattr(event, 'type'):
#         print(f"Event Type: {event.type}")
#     # If the event includes a delta with content, print it
#     if hasattr(event, 'delta') and event.delta:
#         print(f"Delta Content: {event.delta}")
#     # Print a separator for clarity
#     print("-------------------------")

text = ''
for event in stream:
    if event.type == 'response.output_text.delta':
        text += event.delta
    print(text)
