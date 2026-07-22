import sqlite3
import pytest

from langgraph.checkpoint.sqlite import SqliteSaver


@pytest.fixture
def memory_checkpointer():
    conn = sqlite3.connect(":memory:")
    return SqliteSaver(conn)