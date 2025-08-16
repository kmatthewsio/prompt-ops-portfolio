import os, subprocess
from dotenv import load_dotenv

# Load .env but keep shell vars (so BACKEND in shell wins)
load_dotenv(override=False)

BACKEND = os.getenv("BACKEND", "openai").lower()
print(f"Running with BACKEND={BACKEND}")

history = [
    {"role": "user", "content": "knock knock."},
    {"role": "assistant", "content": "Who's there?"},
    {"role": "user", "content": "Orange."}
]

if BACKEND == "openai":
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    resp = client.responses.create(model=model, input=history, store=False)
    print("Assistant response:", resp.output_text)

elif BACKEND == "goose":
    provider = os.getenv("GOOSE_PROVIDER", "ollama")
    model = os.getenv("GOOSE_MODEL", "qwen2.5:3b-instruct-q4_0")
    transcript = "\n".join(f"{m['role']}: {m['content']}" for m in history)
    cmd = ["goose", "run", "--provider", provider, "--model", model, "-t", transcript]
    print(f"Running Goose command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("Assistant response:", result.stdout.strip())

else:
    raise ValueError("Unknown BACKEND")
