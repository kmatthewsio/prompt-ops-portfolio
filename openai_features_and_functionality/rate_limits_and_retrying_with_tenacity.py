import os, requests
from dotenv import load_dotenv
from pathlib import Path

# 1) Load .env FIRST (point to the exact file to avoid CWD surprises)
load_dotenv(dotenv_path=Path("/Users/dove/prompt-ops-portfolio/.env"), override=True)

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in .env or env vars")

headers = {
    "Authorization": f"Bearer {API_KEY.strip()}",
    "Content-Type": "application/json"
}

messages = [{"role": "user", "content": "j"}]
data = {"model": MODEL, "messages": messages, "max_tokens": 1}

resp = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers=headers,
    json=data,
    timeout=30
)

# 2) Fail fast if not 2xx; errors often don't include RL headers
try:
    resp.raise_for_status()
except requests.HTTPError:
    print("HTTP:", resp.status_code)
    print("Body:", resp.text)
    print("Resp headers:", dict(resp.headers))
    raise

# Safe header access
print("Remaining requests:", resp.headers.get("x-ratelimit-remaining-requests"))
print("Remaining tokens:",   resp.headers.get("x-ratelimit-remaining-tokens"))
print("Retry-After:",        resp.headers.get("retry-after"))
print("Reply:", resp.json()["choices"][0]["message"]["content"])
