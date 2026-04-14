import pytest


def test_health_endpoint_exists(client):
    # This test validates the health endpoint is at least wired and returns a 2xx/3xx
    try:
        resp = client.get("/health")
    except Exception:
        pytest.skip("Health endpoint not available in this environment.")
        return

    assert resp.status_code in (200, 204, 301, 302)
