from langchain_core.messages import HumanMessage

from main import workflow


def test_graph_runs():

    config = {
        "configurable": {
            "thread_id": "pytest"
        }
    }

    result = workflow.invoke(
        {
            "messages": [
                HumanMessage(content="What is Python?")
            ]
        },
        config=config
    )

    assert "messages" in result