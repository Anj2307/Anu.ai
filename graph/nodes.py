from graph.state import ChatState
from services.tools import tools, llm_with_tools, llm
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
)

from langgraph.prebuilt import ToolNode

tool_node= ToolNode(tools)

def chat_node(state: ChatState):
    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response]
    }


def title_node(state: ChatState):

    # Generate title only once
    if state.get("title"):
        return {}

    prompt = [
        SystemMessage(
            content="You generate short chat titles."
        ),
        HumanMessage(
            content=f"""
Generate a short 4 to 6 word title for this conversation.

Conversation:
{state["messages"][:4]}

Return only the title.
"""
        ),
    ]

    response = llm.invoke(prompt)

    return {
        "title": response.content
    }