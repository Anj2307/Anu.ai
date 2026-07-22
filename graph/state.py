from typing import TypedDict, Annotated
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
)
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    title: str