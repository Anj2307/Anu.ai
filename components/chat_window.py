import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from main import workflow


def chat_window():
    for message in st.session_state["message_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type here")

    if user_input:

        st.session_state["message_history"].append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        config = {
            "configurable": {
                "thread_id": st.session_state["thread_id"]
            },
            "metadata": {
                "thread_id": st.session_state["thread_id"]
            },
            "run_name" : "chat_trun"
        }

        with st.chat_message("assistant"):

            def response_generator():
                for message_chunk, metadata in workflow.stream(
            {
                "messages": [
                    SystemMessage(content="You are a helpful assistant."),
                    HumanMessage(content=user_input),
                ]
            },
            config=config,
            stream_mode="messages",
        ):
                    if metadata["langgraph_node"] == "chat_node":
                        yield message_chunk.content

        ai_message = st.write_stream(response_generator())

        st.session_state["message_history"].append(
            {
                "role": "assistant",
                "content": ai_message
            }
        )
