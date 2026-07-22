import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver

from graph.graph import graph_maker

conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)

workflow = graph_maker(checkpointer)
