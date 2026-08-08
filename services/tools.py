from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain_core.tools import tool

from utils.config import load_secrets
from utils.llm import initialize_llm

load_dotenv()
load_secrets()

llm = initialize_llm()

search_tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
)


@tool
def calculator(first_num: float, second_num: float, operation: str) -> float:
    """Perform basic arithmetic operations."""
    if operation == "add":
        return first_num + second_num
    elif operation == "subtract":
        return first_num - second_num
    elif operation == "multiply":
        return first_num * second_num
    elif operation == "divide":
        if second_num == 0:
            raise ValueError("Cannot divide by zero.")
        return first_num / second_num
    else:
        raise ValueError(f"Unsupported operation: {operation}")


@tool
def search_documents(query: str) -> str:
    """Search the user's uploaded documents / knowledge base for relevant context.

    Use this whenever the user asks a question about documents, files, notes, or
    any context they have uploaded. Returns the most relevant passages.
    """
    import streamlit as st

    retriever = st.session_state.get("retriever")
    if retriever is None:
        return (
            "No documents have been uploaded yet. Ask the user to upload a "
            "document in the sidebar first."
        )

    docs = retriever.invoke(query)
    if not docs:
        return "No relevant information was found in the uploaded documents."

    return "\n\n---\n\n".join(
        f"[source: {d.metadata.get('source', 'unknown')}]\n{d.page_content}"
        for d in docs
    )


tools = [search_tool, calculator, search_documents]

llm_with_tools = llm.bind_tools(tools)
