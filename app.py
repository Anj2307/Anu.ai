from components.chat_window import chat_window
from components.sidebar import render_sidebar
from utils.session import initialize_session

initialize_session()

render_sidebar()

chat_window()
