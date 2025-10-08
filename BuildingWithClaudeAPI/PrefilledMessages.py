from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
from statistics import mean
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

def run_prompt(test_case):
    """Merge the prompt and test case input, then returns the results"""
    prompt = f"""
Please solve the following task:
{test_case["task"]}
"""
    messages = []
    add_user_messages(messages, prompt)
    output = chat(messages)
    return output

def run_test_case(test_case):
    """ Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)

    score = 10

    return {
        "output": output,
        "test_case": test_case,
        "score": score

    }

def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""

    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)
    return results
    

add_user_messages(messages, prompt)
add_assistant_messages(messages, "```json")
answer = chat(messages, stop_sequences=["```"])

# Strip whitespace before parsing
answer = answer.strip()
#print("Raw answer:", repr(answer))

response = json.loads(answer)

with open("dataset.json", "w") as f:
  dataset =  json.dump(response, f, indent=2)

dataset = response
results = run_eval(dataset)
print(json.dumps(results, indent=2))


