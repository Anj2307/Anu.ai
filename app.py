import streamlit as st

from utils.session import initialize_session
from components.sidebar import render_sidebar
from components.chat_window import chat_window

initialize_session()

render_sidebar()

chat_window()