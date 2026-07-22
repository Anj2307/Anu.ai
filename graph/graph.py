from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import tools_condition

from graph.nodes import chat_node, title_node, tool_node
from graph.state import ChatState


def graph_maker(checkpointer):
    graph = StateGraph(ChatState)

    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)
    graph.add_node("title_node", title_node)

    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges(
        "chat_node", tools_condition, {"tools": "tools", "__end__": "title_node"}
    )
    graph.add_edge("tools", "chat_node")
    graph.add_edge("title_node", END)

    workflow = graph.compile(checkpointer=checkpointer)
    return workflow
