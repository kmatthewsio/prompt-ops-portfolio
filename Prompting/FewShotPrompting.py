from openai import OpenAI
import os
from dotenv import load_dotenv
from venv import create

MODEL = "gpt-4.1-mini"

load_dotenv()  # Load environment variables from .env file

# Create an OpenAI client instance
client = OpenAI(
    # Replace with your actual API key or use: api_key=os.environ.get("OPENAI_API_KEY")
    api_key= os.getenv("OPENAI_API_KEY"))

def zero_shot(question):
    """No examples - just ask the question"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
        max_tokens=200
    )
    return response.choices[0].message.content


def few_shot(question):
    """Give examples first, then ask the question"""

    prompt = """Convert these sentences to a more professional tone:

Example 1:
Input: "Hey, can you fix this bug? It's kinda broken."
Output: "Could you please address this software defect? The functionality appears to be compromised."

Example 2:
Input: "This meeting was totally useless."
Output: "This meeting did not yield the expected outcomes."

Example 3:
Input: "The code is a mess and needs work."
Output: "The codebase requires refactoring and optimization."

Now convert this sentence:
""" + question

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content


# Test the difference
test_sentence = "This app crashes all the time and is super annoying."

print("Zero-Shot (no examples):")
zero_result = zero_shot(f"Make this more professional: {test_sentence}")
print(zero_result)
print()

print("Few-Shot (with examples):")
few_result = few_shot(test_sentence)
print(few_result)
print()

email_classification_prompt = """Classify these emails as SPAM or LEGITMATE:

Example 1:
Email: "URGENT: You've won $1,000,000! Click here now!"
Classification: SPAM

Example 2:
Email: "Meeting reminder: Project review at 3 PM tomorrow"
Classification: LEGITIMATE

Example 3:
Email: "FREE VIAGRA!!! Limited time offer!!!"
Classification: SPAM

Now classify this email:
Email: "Your package delivery is scheduled for today between 2-4 PM"
Classification:"""

classification_result = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": email_classification_prompt}],
        max_tokens=50
    ).choices[0].message.content

print("Email Classifications:")
print(classification_result)
