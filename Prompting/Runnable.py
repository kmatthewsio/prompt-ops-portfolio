from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from venv import create
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

#LangChain Expression Language (LCEL) and the Runnable Protocol are used to build chains in LangChain
#Optimized parallel execution
#Guaranteed async support
#Seamless LangSmith tracing
#Simplified streaming

# Old way (deprecated)
# chain = LLMChain(llm=llm, prompt=prompt)
# New way with pipe operator - The | (pipe) operator chains Runnables together,
# where each component implements the Runnable interface
#chain = prompt | llm | output_parser
MODEL = "gpt-4.1-mini"

load_dotenv()  # Load environment variables from .env file

llm = ChatOpenAI(
    api_key= os.getenv("OPENAI_API_KEY"))

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful {role}"),
    ("human", "{question}")
])

output_parser = StrOutputParser()

#old way
def old_way(role, question):
    formatted_prompt = prompt.format_messages(role=role, question=question)
    response = llm.invoke(formatted_prompt)
    parsed = output_parser.parse(response.content)
    return parsed


chain = prompt | llm | output_parser
def new_way(role, question):
    return chain.invoke({
        "role": role,
        "question" : question
    })

print("Old way")
result1 = old_way("Python", "What are variables?")
print(result1)

print("New way using langchain expression language")
result2 = new_way("Python tutor", "What are vaiables?")
print(result2)


