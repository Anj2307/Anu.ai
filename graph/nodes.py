from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode

from graph.state import ChatState
from services.tools import llm, llm_with_tools, tools

tool_node = ToolNode(tools)


def chat_node(state: ChatState):
    response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


def title_node(state: ChatState):

    # Generate title only once
    if state.get("title"):
        return {}

    prompt = [
        SystemMessage(content="You generate short chat titles."),
        HumanMessage(content=f"""
Generate a short 4 to 6 word title for this conversation.

Conversation:
{state["messages"][:4]}

Return only the title.
"""),
    ]

    response = llm.invoke(prompt)

    return {"title": response.content}


def route(state: ChatState):
    user_msg = state["messages"][-1].content

    prompt = [
        SystemMessage(
            content=(
                "You are an intent classifier. Reply with EXACTLY one word: "
                "'calculator' if the user is asking for an arithmetic "
                "calculation, otherwise 'chat'. Return only that word."
            )
        ),
        HumanMessage(content=user_msg),
    ]

    # Plain-text classification (no structured output) so it works reliably
    # even when the response is streamed through a lightweight free model.
    # Falls back to "chat" if the model misbehaves.
    try:
        response = llm.invoke(prompt)
        text = (response.content or "").strip().lower()
        intent = "calculator" if "calculator" in text else "chat"
    except Exception:
        intent = "chat"

    return {"intent": intent}


def router_condition(state: ChatState):

    mapping = {"chat": "chat_node", "calculator": "chat_node"}
    return mapping[state["intent"]]
