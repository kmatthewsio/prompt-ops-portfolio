from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
import json

client = Anthropic()
model = "claude-sonnet-4-0"

def add_user_messages(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_messages(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences
    }
    
    if system:
        params["system"] = system
    
    message = client.messages.create(**params)
    return message.content[0].text

# Main execution at module level
messages = []
prompt = """ 
Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing task that requires Python, JSON, or a Regex to complete.

Example output:
[
    {
        "task": "Description of task",
    }
]

Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
Please generate 3 objects.
"""

add_user_messages(messages, prompt)
add_assistant_messages(messages, "```json")
answer = chat(messages, stop_sequences=["```"])

# Strip whitespace before parsing
answer = answer.strip()
print("Raw answer:", repr(answer))

response = json.loads(answer)

with open("dataset.json", "w") as f:
    json.dump(response, f, indent=2)  # Changed: json.dump() not json.dumps()

print("Dataset saved to dataset.json")