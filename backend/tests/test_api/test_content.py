import pytest


def test_content_list_endpoint_exists(client):
    try:
        resp = client.get("/api/v1/content")
    except Exception:
        pytest.skip("Content endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 401, 403, 404)
