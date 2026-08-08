from components.chat_window import chat_window
from components.sidebar import render_sidebar
from utils.auth import require_login
from utils.session import initialize_session

require_login()

initialize_session()

render_sidebar()

chat_window()
