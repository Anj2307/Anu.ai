import streamlit as st

from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage

from utils.frontend import load_conversation


def load_messages_into_session(thread_id):

    st.session_state["thread_id"] = thread_id

    messages = load_conversation(thread_id)

    history = []

    for msg in messages:

        if isinstance(msg, HumanMessage):
            role = "user"

        elif isinstance(msg, SystemMessage):
            continue

        else:
            role = "assistant"

        history.append(
            {
                "role": role,
                "content": msg.content
            }
        )

    st.session_state["message_history"] = history