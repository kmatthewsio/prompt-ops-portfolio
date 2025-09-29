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

messages = []

add_user_messages(messages, "Write a 1 senctence descripton of a fake database.")

stream = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    stream=True
)

#for event in stream:
 #print(event)

#get the actual text we need from RawContentBlockDeltaEvent
with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages
) as stream:
    for text in stream.text_stream:
        #print(text, end="")
        pass

finalmessage = stream.get_final_message()
print(finalmessage)