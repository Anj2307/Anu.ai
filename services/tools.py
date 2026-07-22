from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition

from utils.llm import initialize_llm

llm = initialize_llm()
search_tool = DuckDuckGoSearchRun(region="us-en")


@tool
def calculator(first_num: float, second_num: float, operation: str) -> float:
    """ "
    A simple calculator tool that performs basic arithmetic operations."""
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
