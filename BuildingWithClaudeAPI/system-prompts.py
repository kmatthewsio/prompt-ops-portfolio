from dotenv import  load_dotenv
load_dotenv()

from anthropic import Anthropic
client = Anthropic()
model = "claude-sonnet-4-0"

def add_user_messages(messages, text):
    user_message ={"role": "user", "content": text}
    messages.append(user_message)
def add_assistant_messages(messages, text):
    assistant_message = {"role": "user", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "system": system
    }

    if system:
        params["system"] = system
    message = client.messages.create(**params)
    return message.content[0].text

messages = []

system = """
    You are a python engineer who writes very concise code.
    """
add_user_messages(messages, "Write a python function that checks a string for duplicate characters")
answer = chat(messages, system=system)

print(answer)






