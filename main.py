import os
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver

from graph.graph import graph_maker

# Streamlit Community Cloud has an ephemeral filesystem, so this db does not
# persist across restarts. CHATBOT_DB_PATH lets you point it elsewhere.
DB_PATH = os.getenv("CHATBOT_DB_PATH", "chatbot.db")

conn = sqlite3.connect(database=DB_PATH, check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)

workflow = graph_maker(checkpointer)
