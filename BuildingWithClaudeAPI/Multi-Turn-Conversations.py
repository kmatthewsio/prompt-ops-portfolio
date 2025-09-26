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

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages
    )
    return message.content[0].text

#start with empty message list
messages = []
#add the inital question
add_user_messages(messages, "Define quantum computing in once sentence")
answer = chat(messages)
#add response to conversation history
add_assistant_messages(messages, answer)
#ask a follow on question
add_user_messages(messages, "Write another sentence")
#get the answer
final_answer = chat(messages)


messages2 = []

while True:
    user_input = input(">")
    print(">", user_input)

    add_user_messages(messages2, user_input)
    answer2 = chat(messages2)
    add_assistant_messages(messages2, answer2)

    print("---")
    print(answer2)
    print("---")
