from dotenv import  load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()
model = "claude-sonnet-4-0"

message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {
        "role": "user",
        "content": "What is quantum computing? Answer in one sentence"
        }
    ]
)



print(message.content[0].text)

