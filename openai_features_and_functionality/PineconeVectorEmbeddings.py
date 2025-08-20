from openai import OpenAI
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from venv import create

MODEL = "gpt-4.1-mini"

load_dotenv()  # Load environment variables from .env file

# Create an OpenAI client instance
client = OpenAI(
   api_key = os.getenv("OPENAI_API_KEY")
)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

def text_to_vector(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        dimensions=1024
    )

    return response.data[0].embedding # numerical representation of text (computers can't compare meaning but they
                                      # can compare numbers so "I love dogs" becomes [0.3, -0.7, 0.2, ...]
def store_knowledge(text, id):
    vector = text_to_vector(text)
    index.upsert( [{
        "id": id,
        "values": vector,
        "metadata":
        {
            "text": text
        }
    }])

    print(f"Stored: {text}")

def find_similar(question):
    question_vector = text_to_vector(question)
    results = index.query(vector=question_vector, top_k=3, include_metadata=True)

    print(f"Question: {question}")
    for match in results['matches']:
        print(f"  Similar: {match['metadata']['text']} (score: {match['score']:.2f})")

# Example usage
print("=== Storing Knowledge ===")
store_knowledge("Python is a programming language", "fact1")
store_knowledge("Dogs are animals that bark", "fact2")
store_knowledge("Pizza is a food with cheese", "fact3")

print("\n=== Finding Similar ===")
find_similar("What programming languages exist?")
find_similar("Tell me about pets")
