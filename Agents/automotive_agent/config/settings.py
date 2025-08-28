import os
from dotenv import load_dotenv

load_dotenv()

# Simple settings - just what we need
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4.1-mini"

