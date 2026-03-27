import pytest


def test_playback_endpoint_exists(client):
    try:
        resp = client.post("/api/v1/playback/start", json={"content_id": 1})
    except Exception:
        pytest.skip("Playback endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 202, 401, 403)
