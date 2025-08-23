from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from venv import create
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

MODEL = "gpt-4.1-mini"

load_dotenv()  # Load environment variables from .env file

llm = ChatOpenAI(
    api_key= os.getenv("OPENAI_API_KEY"))

# returns unstructured text
def without_parsing():
    response = llm.invoke("Tell me a about python programming")
    print("Without parsing (just exit:)")
    print(type(response.content))
    print(response.content)
    print()

def with_json_parsing():
    parser = JsonOutputParser()
    template = ChatPromptTemplate.from_messages([
        ("human", "Tell me about {topic}. {format_instructions}")
    ])

    prompt = template.format_messages(
        topic = "Python programming",
        format_instructions=parser.get_format_instructions()
    )

    response = llm.invoke(prompt)
    parsed = parser.parse(response.content)
    print("With JSON parsing (structured data):")
    print(type(parsed))
    print(parsed)
    print()

class PersonInfo(BaseModel):
    name: str = Field(description="Person's full name")
    age: int = Field(description="Person's age")
    occupation: str = Field(description="Person's job")
    skills: list[str] = Field(description="List of skills")
def with_pydantic_parsing():
    parser = PydanticOutputParser(pydantic_object=PersonInfo)

    template = ChatPromptTemplate.from_messages([
        ("human", "Create a profile for a software developer named John. {format_instructions}")
    ])

    prompt = template.format_messages(
        format_instructions=parser.get_format_instructions()
    )

    response = llm.invoke(prompt)
    parsed = parser.parse(response.content)

    print("With Pydantic parsing (typed objects):")
    print(type(parsed))
    print(f"Name: {parsed.name}")
    print(f"Age: {parsed.age}")
    print(f"Skills: {parsed.skills}")
    print()

without_parsing()
with_json_parsing()
with_pydantic_parsing()