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

def ask_ai(prompt):
    """Simple helper to ask AI"""
    response = client.chat.completions.create(
        model=MODEL,
        messages= [{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return response.choices[0].message.content

def tutor_templates(student_name, topic):
    return f""" You are a helpful tutor for {student_name}.

Explain {topic} in simple terms that a begginer can understand.
Use examples and analogies to make it clear.
Keep your explinatons under 200 words.
"""

def email_template(tone, recipient, subject, context):
    return f"""Write a {tone} email to {recipient} about {subject}.

Context: {context}
Keep it professional and clear."""

def code_review_template(language, code, focus):
    return f"""Review this {language}code:
```{language}
{code}
```
Focus on: {focus}
Provide specifc, actionable feedback. """

print("Simple Template Approach")
print('1. Tutor Template:')
tutor_prompt = tutor_templates("Sarah", "Python variables")
print(f"Prompt: {tutor_prompt}")
print()
response = ask_ai(tutor_prompt)
print(f"Response: {response}")
print("\n" + "="*50 + "\n")

print("2. Email Template:")
email_prompt = email_template(
    tone="friendly",
    recipient="my colleagues",
    subject="team meeting",
    context="We need to discuss the new project timeline"
)
print(f"Prompt: {email_prompt}")
print()
response = ask_ai(email_prompt)
print(f"Response: {response}")
print("\n" + "="*50 + "\n")