import os
import pytest


@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: ensure test-specific environment is clean
    os.environ.setdefault("TESTING", "1")
    yield
    # Teardown: clean up if needed
    os.environ.pop("TESTING", None)


def test_testing_config_enabled():
    assert os.environ.get("TESTING") == "1"


def test_sqlite_in_memory_connection():
    import sqlite3
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("SELECT 1")
    assert cur.fetchone()[0] == 1
    cur.close()
    conn.close()
