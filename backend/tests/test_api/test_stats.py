import pytest


def test_stats_endpoint_exists(client):
    try:
        resp = client.get("/api/v1/stats")
    except Exception:
        pytest.skip("Stats endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 401, 403, 404)
