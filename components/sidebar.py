import streamlit as st

from components.conversation import load_messages_into_session
from utils.frontend import get_title, load_conversation, reset_chat


def render_sidebar():

    st.sidebar.title("LangGraph Chatbot")

    if st.sidebar.button("New Chat"):
        reset_chat()

    st.sidebar.header("My Conversations")

    for thread in st.session_state["chat_threads"]:

        if st.sidebar.button(get_title(thread), key=thread):

            load_messages_into_session(thread)

            st.rerun()
