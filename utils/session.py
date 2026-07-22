import streamlit as st

from utils.frontend import (
    generate_thread_id,
    add_thread
)

from langgraph_backend_database import retreive_all_threads


def initialize_session():

    if "message_history" not in st.session_state:
        st.session_state["message_history"] = []

    if "thread_id" not in st.session_state:
        st.session_state["thread_id"] = generate_thread_id()

    if "chat_threads" not in st.session_state:
        st.session_state["chat_threads"] = retreive_all_threads()

    add_thread(st.session_state["thread_id"])