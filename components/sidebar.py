import streamlit as st

from components.conversation import load_messages_into_session
from utils.auth import logout
from utils.frontend import get_title, reset_chat


def render_sidebar():

    st.sidebar.title("LangGraph Chatbot")
    st.sidebar.caption(f"Logged in as **{st.session_state['user_id']}**")

    col1, col2 = st.sidebar.columns(2)

    if col1.button("New Chat"):
        reset_chat()

    if col2.button("Log out"):
        logout()

    st.sidebar.header("My Conversations")

    for thread in st.session_state["chat_threads"]:

        if st.sidebar.button(get_title(thread), key=thread):

            load_messages_into_session(thread)

            st.rerun()
