from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from venv import create

MODEL = "gpt-4.1-mini"

load_dotenv()  # Load environment variables from .env file

llm = ChatOpenAI(
    api_key= os.getenv("OPENAI_API_KEY"))

template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}"),
    ("human", "{question}")
])

response = llm.invoke(template.format_messages (
    role="helpful assistant",
    question="What is Python?"
))

print (response.content)
