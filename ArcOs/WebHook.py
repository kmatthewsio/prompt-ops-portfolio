# send_webhook_json.py
import json
import time
import requests  # pip install requests

WEBHOOK_URL = "https://hook.us2.make.com/1ieplgeyqf22q40rivib3whjyyd84bo4"

payload = {
    "task": "Write demo",
    "priority": "high",
    "due": "2025-09-10T17:00:00Z",
    "source": "python-requests",
    "sent_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
}

headers = {
    "Content-Type": "application/json",
    # Optional shared secret header (add a Make filter to check it):
    # "X-Webhook-Secret": "supersecret123",
}

resp = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(payload), timeout=15)
print("Status:", resp.status_code)
# If you added a “Webhook response” module in Make, you’ll see JSON here:
print("Body:", resp.text)
