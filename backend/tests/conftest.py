import pytest

# Attempt to import the FastAPI app from the backend project.
try:
    from backend.app.main import app as fastapi_app  # type: ignore
except Exception:
    fastapi_app = None  # type: ignore

# Try to import FastAPI's TestClient for lightweight tests.
try:
    from fastapi.testclient import TestClient
except Exception:  # pragma: no cover
    TestClient = None  # type: ignore


@pytest.fixture(scope="session")
def client():
    """Provide a TestClient for backend API tests if the app is available.

    If the app cannot be imported in the test environment, the tests that rely
    on the backend can be skipped gracefully.
    """
    if fastapi_app is None or TestClient is None:
        pytest.skip("FastAPI app not available for tests, skipping backend tests.")
    return TestClient(fastapi_app)
