import sqlite3
from contextlib import closing


def in_memory_connection():
    conn = sqlite3.connect(":memory:")
    return conn
