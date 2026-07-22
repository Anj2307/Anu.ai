import uuid

import streamlit as st

from main import workflow



def generate_thread_id():
    return str(uuid.uuid4())


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def reset_chat():
    thread_id = generate_thread_id()

    st.session_state["thread_id"] = thread_id
    st.session_state["message_history"] = []

    add_thread(thread_id)

    st.rerun()


def get_title(thread_id):
    state = workflow.get_state(config={"configurable": {"thread_id": thread_id}})

    return state.values.get("title", f"Chat {thread_id[:8]}")


def load_conversation(thread_id):
    state = workflow.get_state(config={"configurable": {"thread_id": thread_id}})

    return state.values.get("messages", [])
