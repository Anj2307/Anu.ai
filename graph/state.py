from typing import Annotated, TypedDict, Literal
from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    title: str
    intent: str

class Intent(BaseModel):
    intent: Literal["chat","calculator"]