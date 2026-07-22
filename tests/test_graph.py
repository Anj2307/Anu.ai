from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage, HumanMessage

from main import workflow


@patch("graph.nodes.llm")
@patch("graph.nodes.llm_with_tools")
def test_graph_runs(mock_llm_with_tools, mock_llm):

    mock_llm_with_tools.invoke.return_value = AIMessage(
        content="Python is a programming language."
    )

    mock_llm.invoke.return_value = MagicMock(content="Python Chat")

    config = {"configurable": {"thread_id": "pytest"}}

    result = workflow.invoke(
        {"messages": [HumanMessage(content="What is Python?")]},
        config=config,
    )

    assert "messages" in result
