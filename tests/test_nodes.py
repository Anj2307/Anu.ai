from unittest.mock import MagicMock, patch

from langchain_core.messages import HumanMessage

from graph.nodes import chat_node, title_node


@patch("graph.nodes.llm_with_tools")
def test_chat_node(mock_llm):

    fake_response = MagicMock()

    fake_response.content = "Hello"

    mock_llm.invoke.return_value = fake_response

    state = {"messages": [HumanMessage(content="Hi")], "title": ""}

    result = chat_node(state)

    assert "messages" in result
    assert len(result["messages"]) == 1


@patch("graph.nodes.llm")
def test_title_node(mock_llm):

    fake_response = MagicMock()

    fake_response.content = "Greeting Chat"

    mock_llm.invoke.return_value = fake_response

    state = {"messages": [HumanMessage(content="Hello")], "title": ""}

    result = title_node(state)

    assert result["title"] == "Greeting Chat"


def test_title_not_generated_twice():

    state = {"messages": [], "title": "Existing Title"}

    result = title_node(state)

    assert result == {}
