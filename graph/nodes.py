from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode

from graph.state import ChatState
from services.tools import llm, llm_with_tools, tools, vision_llm

tool_node = ToolNode(tools)


def _extract_text(content):
    """Plain-text part of a message content (which may be a list of multimodal
    parts for image messages)."""
    if isinstance(content, list):
        return " ".join(
            part.get("text", "")
            for part in content
            if isinstance(part, dict) and part.get("type") == "text"
        ).strip()
    return content or ""


def _has_image(message):
    content = getattr(message, "content", None)
    if isinstance(content, list):
        return any(
            isinstance(part, dict) and part.get("type") == "image_url"
            for part in content
        )
    return False


def chat_node(state: ChatState):
    # Image messages go to the multimodal model (not tool-bound); everything
    # else uses the normal tool-enabled chat model.
    if _has_image(state["messages"][-1]):
        response = vision_llm.invoke(state["messages"])
    else:
        response = llm_with_tools.invoke(state["messages"])

    return {"messages": [response]}


def title_node(state: ChatState):

    # Generate title only once
    if state.get("title"):
        return {}

    transcript = []
    for message in state["messages"][:4]:
        text = _extract_text(getattr(message, "content", ""))
        if text:
            transcript.append(f"{message.__class__.__name__}: {text}")

    prompt = [
        SystemMessage(content="You generate short chat titles."),
        HumanMessage(
            content=(
                "Generate a short 4 to 6 word title for this conversation.\n\n"
                "Conversation:\n" + "\n".join(transcript) + "\n\nReturn only the title."
            )
        ),
    ]

    response = llm.invoke(prompt)

    return {"title": response.content}


def route(state: ChatState):
    user_msg = _extract_text(state["messages"][-1].content)

    prompt = [
        SystemMessage(
            content=(
                "You are an intent classifier. Reply with EXACTLY one word: "
                "'calculator' if the user is asking for an arithmetic "
                "calculation, otherwise 'chat'. Return only that word."
            )
        ),
        HumanMessage(content=user_msg or "chat"),
    ]

    # Plain-text classification (no structured output) so it works reliably even
    # when streamed through a lightweight free model. Falls back to "chat".
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
