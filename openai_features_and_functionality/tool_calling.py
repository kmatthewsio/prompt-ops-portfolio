
import os, requests
import json
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI

# 1) Load .env FIRST (point to the exact file to avoid CWD surprises)
load_dotenv(dotenv_path=Path("/Users/dove/prompt-ops-portfolio/.env"), override=True)

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY")
)

#Function calling provides a powerful and flexible way for OpenAI models to interface with your code or external services. It allows models to fetch data and take actions by calling functions you define—effectively extending the model’s capabilities. In this notebook, we cover several examples:

#Get Weather: Retrieve the current temperature using provided coordinates.
#Send Email: Simulate sending an email message.
#Search Knowledge Base: Query a knowledge base for information.
#Web Search: Use a web search tool to retrieve recent news or other content.


def get_weather(latitude, longitude):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data['current']['temperature_2m']

    #Tool Calling Overview: Tool calling enables your model to trigger custom functions based on conversation context. Use it to fetch data or perform actions.
    #Defining Functions: Define your functions in the tools parameter using JSON schema. Always set additionalProperties to false and enable strict mode for more reliable results.
    #Handling Responses: When the model calls a function, it returns a function call object (with attributes like type and arguments). Access attributes with dot notation (e.g. tool_call.arguments).


tools = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get current tempature for provided coordinates in celsius.",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number", "description": "Latitude of the location."},
            "longitude":{"type": "number", "description": "Longitude of the location"},
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    },
    "strict": True
 }]

input_messages = [
    {
        "role": "user",
        "content": "What's the weather link in Atlanta Georgia today?"
    }
]

response = client.responses.create(
    model=MODEL,
    input=input_messages,
    tools=tools
)

print("Get Weather Response Output:", response.output)

if response.output and response.output[0].type == "function_call":
    tool_call = response.output[0]
    args = json.loads(tool_call.arguments)
    weather_result = get_weather(args['latitude'], args['longitude'])
    print(f"Weather result: {weather_result}°C")

input_messages.append(tool_call)
input_messages.append({
    "type": "function_call_output",
    "call_id": tool_call.call_id,
    "output": str(json.dumps(weather_result))
})

response = client.responses.create(
    model=MODEL,
    input=input_messages,
    tools=tools
)

print("Get Weather Response Output:", response.output_text)
