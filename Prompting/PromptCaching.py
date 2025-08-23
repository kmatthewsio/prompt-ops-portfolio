import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Long system prompt that you'll reuse many times
LONG_SYSTEM_PROMPT = """You are a Python coding expert. Here are the coding standards you must follow:

1. Use descriptive variable names
2. Add docstrings to all functions
3. Follow PEP 8 style guide
4. Use type hints
5. Handle exceptions properly
6. Write clean, readable code
7. Add comments for complex logic
8. Use meaningful function names
9. Keep functions small and focused
10. Follow SOLID principles

Additional context:
- Always consider performance implications
- Prefer built-in functions over custom solutions
- Use list comprehensions when appropriate
- Follow the DRY principle (Don't Repeat Yourself)
- Write defensive code with proper validation
- Consider edge cases in your solutions
- Use appropriate data structures for the task
- Optimize for readability first, performance second
- Follow consistent naming conventions throughout
- Document any complex algorithms or business logic

Now help the user with their Python coding questions following these standards."""

def code_help_without_caching(question):
    """Standard API call - pays for the full prompt every time"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": LONG_SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        max_tokens=300
    )

    # Return response and usage info
    return response.choices[0].message.content, response.usage


def code_help_with_caching(question):
    """With prompt caching - saves money on repeated system prompts"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": LONG_SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"}  # Cache this part
                    }
                ]
            },
            {"role": "user", "content": question}
        ],
        max_tokens=300
    )

    # Return response and usage info
    return response.choices[0].message.content, response.usage


# Example usage
questions = [
    "How do I read a CSV file?",
    "How do I handle exceptions in Python?",
    "How do I create a class?"
]

# Track costs
total_tokens_without_cache = 0
total_tokens_with_cache = 0
cached_tokens_used = 0

print("=== Without Caching (pays full price each time) ===")
for i, question in enumerate(questions, 1):
    print(f"Question {i}: {question}")
    answer, usage = code_help_without_caching(question)
    total_tokens_without_cache += usage.total_tokens
    print(f"Answer: {answer[:100]}...")
    print(f"Tokens used: {usage.total_tokens}")
    print()

print("=== With Caching (saves money on repeated prompts) ===")
for i, question in enumerate(questions, 1):
    print(f"Question {i}: {question}")
    answer, usage = code_help_with_caching(question)
    total_tokens_with_cache += usage.total_tokens

    # Track cached tokens if available
    if hasattr(usage, 'cached_tokens') and usage.cached_tokens:
        cached_tokens_used += usage.cached_tokens

    print(f"Answer: {answer[:100]}...")
    print(f"Tokens used: {usage.total_tokens}")
    if hasattr(usage, 'cached_tokens'):
        print(f"Cached tokens: {usage.cached_tokens or 0}")
    print()

print("=== Cost Comparison ===")
print(f"Total tokens without caching: {total_tokens_without_cache}")
print(f"Total tokens with caching: {total_tokens_with_cache}")
print(f"Cached tokens reused: {cached_tokens_used}")

if total_tokens_without_cache > 0:
    savings_percent = ((total_tokens_without_cache - total_tokens_with_cache) / total_tokens_without_cache) * 100
    print(f"Token savings: {savings_percent:.1f}%")

    # Rough cost calculation (GPT-4.1-mini: $0.40 per 1M input tokens)
    cost_without = (total_tokens_without_cache / 1_000_000) * 0.40
    cost_with = (total_tokens_with_cache / 1_000_000) * 0.40
    cost_savings = cost_without - cost_with

    print(f"Estimated cost without caching: ${cost_without:.6f}")
    print(f"Estimated cost with caching: ${cost_with:.6f}")
    print(f"Money saved: ${cost_savings:.6f}")

print("\n=== Key Insight ===")
print("The more you reuse the same long prompt, the bigger the savings!")