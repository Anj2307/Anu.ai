import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from graph.state import Intent

def initialize_llm():
    load_dotenv()

    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="openrouter/free",
    )

    return llm

router_llm= initialize_llm().with_structured_output(Intent)