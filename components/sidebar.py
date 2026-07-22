import streamlit as st

from utils.frontend import (
    reset_chat,
    get_title,
    load_conversation
)

from components.conversation import load_messages_into_session


def render_sidebar():

    st.sidebar.title("LangGraph Chatbot")

    if st.sidebar.button("New Chat"):
        reset_chat()

    st.sidebar.header("My Conversations")

    for thread in st.session_state["chat_threads"]:

        if st.sidebar.button(get_title(thread), key=thread):

            load_messages_into_session(thread)

            st.rerun()