import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

MODEL = "gpt-4.1-mini"  # or "gpt-4o"

load_dotenv()

# one async client for the whole module
aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def get_chat_response(prompt: str) -> str:
    resp = await aclient.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return resp.choices[0].message.content


async def main():
    prompt = "What is the capital of Vietnam?"
    print(await get_chat_response(prompt))


if __name__ == "__main__":
    asyncio.run(main())
