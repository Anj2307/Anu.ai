from typing import Annotated, Literal, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    title: str
    intent: str


class Intent(BaseModel):
    intent: Literal["chat", "calculator"]
