import os
from dotenv import load_dotenv
from langsmith import traceable
from openai import OpenAI

MODEL = "gpt-4.1-mini"
LANGMSITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

load_dotenv()  # Load environment variables from .env file

client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY"))


# Without tracing: No visibility
def ask_ai_basic(question):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content


# With tracing: Just add @traceable decorator
@traceable
def ask_ai_traced(question):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content


# Trace complex workflows
@traceable
def research_topic(topic):
    # Step 1: Generate questions
    questions = generate_questions(topic)

    # Step 2: Answer each question
    answers = []
    for q in questions:
        answer = ask_ai_traced(q)
        answers.append(answer)

    # Step 3: Summarize
    summary = summarize_answers(answers)
    return summary


@traceable
def generate_questions(topic):
    prompt = f"Generate 3 research questions about {topic}"
    response = ask_ai_traced(prompt)
    return response.split('\n')


@traceable
def summarize_answers(answers):
    all_answers = '\n'.join(answers)
    prompt = f"Summarize these answers: {all_answers}"
    return ask_ai_traced(prompt)


# Example usage
print("=== Modular Tracing with @traceable ===")

# This gets traced automatically
result = research_topic("Python programming")
print(f"Result: {result}")

