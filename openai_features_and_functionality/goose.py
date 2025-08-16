# knockknock_goose.py
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()  # if you want to set GOOSE_* via .env

# Use your working Goose/Ollama setup
GOOSE_PROVIDER = os.getenv("GOOSE_PROVIDER", "ollama")
GOOSE_MODEL    = os.getenv("GOOSE_MODEL", "qwen2.5:3b-instruct-q4_0")

# Construct a conversation history manually for a knock-knock joke
history = [
    {"role": "user", "content": "knock knock."},
    {"role": "assistant", "content": "Who's there?"},
    {"role": "user", "content": "Orange."}
]

# Flatten the chat history into a single prompt for Goose CLI
transcript = "\n".join(f"{m['role']}: {m['content']}" for m in history)

# Call Goose (which talks to your local Ollama model)
result = subprocess.run(
    [
        "goose", "run",
        "--provider", GOOSE_PROVIDER,
        "--model", GOOSE_MODEL,
        "-t", transcript,
        # Optional tweaks:
        # "--num_ctx", "1024",
        # "--temperature", "0.7",
    ],
    capture_output=True,
    text=True,
    check=True
)

print("Assistant response:", result.stdout.strip())
