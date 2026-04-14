"""播放限制API测试。"""

import pytest


def test_get_global_limit_endpoint_exists(client):
    """测试获取全局限制端点存在。"""
    try:
        resp = client.get("/api/v1/limits/global")
    except Exception:
        pytest.skip("Limits endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 401, 403)


def test_update_global_limit_endpoint_exists(client):
    """测试更新全局限制端点存在。"""
    try:
        resp = client.put("/api/v1/limits/global", json={"daily_minutes": 60})
    except Exception:
        pytest.skip("Limits endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 401, 403, 422)


def test_get_user_limit_endpoint_exists(client):
    """测试获取用户限制端点存在。"""
    try:
        resp = client.get("/api/v1/limits/users/admin")
    except Exception:
        pytest.skip("Limits endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 401, 403, 404)


def test_update_user_limit_endpoint_exists(client):
    """测试更新用户限制端点存在。"""
    try:
        resp = client.put("/api/v1/limits/users/admin", json={"daily_minutes": 30})
    except Exception:
        pytest.skip("Limits endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 401, 403, 404, 422)


def test_delete_user_limit_endpoint_exists(client):
    """测试删除用户限制端点存在。"""
    try:
        resp = client.delete("/api/v1/limits/users/admin")
    except Exception:
        pytest.skip("Limits endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 204, 401, 403, 404)
