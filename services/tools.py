from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from langchain_core.tools import tool

from utils.llm import initialize_llm

load_dotenv()

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


tools = [search_tool, calculator]

llm_with_tools = llm.bind_tools(tools)
