from openai import OpenAI
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from venv import create
from supabase import create_client

MODEL = "gpt-4.1-mini"

load_dotenv()  # Load environment variables from .env file

# Create an OpenAI client instance
client = OpenAI(
   api_key = os.getenv("OPENAI_API_KEY")
)

supabase = create_client(
    "https://upihmcqbxriwrtidkoqe.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVwaWhtY3FieHJpd3J0aWRrb3FlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU2NTA0NDQsImV4cCI6MjA3MTIyNjQ0NH0.Wv4BGkjBMy_aR8PlhRQGRFAlC-HfqkJItOAPplx2THI"
)


def text_to_vector(text):
    # Turn text into vector
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        dimensions=1024
    )
    return response.data[0].embedding


def store_document(text, title):
    # Check if document already exists
    existing = supabase.table("documents").select("id").eq("title", title).execute()

    if existing.data:
        print(f"Already exists: {title}")
        return

    # Store new document
    vector = text_to_vector(text)
    result = supabase.table("documents").insert({
        "title": title,
        "content": text,
        "embedding": vector
    }).execute()

    print(f"Stored: {title}")


def find_relevant_docs(question, limit=3):
    # Find documents similar to the question
    question_vector = text_to_vector(question)

    # Use Supabase's vector similarity search
    result = supabase.rpc("match_documents", {
        "query_embedding": question_vector,
        "match_count": limit
    }).execute()

    print(f"Found {len(result.data)} similar documents")

    return result.data


def answer_with_context(question):
    # RAG: Retrieve relevant docs, then Generate answer

    print(f"Question: {question}")

    # RETRIEVE: Find relevant documents
    relevant_docs = find_relevant_docs(question)

    if not relevant_docs:
        return "No relevant information found."

    # Build context from retrieved documents
    context = "\n\n".join([doc["content"] for doc in relevant_docs])

    print(f"Found {len(relevant_docs)} relevant documents")

    # GENERATE: Answer using the context
    prompt = f"""Answer the question based on this context:

Context:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content


# Example usage
print("=== Storing Documents ===")
store_document("Python is a programming language known for simplicity", "Python Facts")
store_document("Machine learning uses algorithms to find patterns", "ML Basics")
store_document("Databases store and organize information", "Database Info")

print("\n=== RAG Question Answering ===")
answer = answer_with_context("What is Python used for?")
print(f"Answer: {answer}")