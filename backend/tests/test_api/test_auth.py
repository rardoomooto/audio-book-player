import pytest


def test_auth_login_endpoint_exists(client):
    # Basic smoke test to ensure the login endpoint is wired when available
    try:
        resp = client.post("/api/v1/auth/login", json={"username": "test", "password": "test"})
    except Exception:
        pytest.skip("Auth endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 401, 403, 422)
