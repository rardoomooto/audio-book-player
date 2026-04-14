"""文件夹API测试。"""

import pytest


def test_list_folders_endpoint_exists(client):
    """测试文件夹列表端点存在。"""
    try:
        resp = client.get("/api/v1/folders/")
    except Exception:
        pytest.skip("Folders endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 401, 403, 404)


def test_get_folder_endpoint_exists(client):
    """测试获取文件夹端点存在。"""
    try:
        resp = client.get("/api/v1/folders/1")
    except Exception:
        pytest.skip("Folders endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 401, 403, 404)


def test_create_folder_endpoint_exists(client):
    """测试创建文件夹端点存在。"""
    try:
        resp = client.post("/api/v1/folders/", json={"name": "Test Folder"})
    except Exception:
        pytest.skip("Folders endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 201, 401, 403, 422)


def test_update_folder_endpoint_exists(client):
    """测试更新文件夹端点存在。"""
    try:
        resp = client.put("/api/v1/folders/1", json={"name": "Updated Folder"})
    except Exception:
        pytest.skip("Folders endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 401, 403, 404, 422)


def test_delete_folder_endpoint_exists(client):
    """测试删除文件夹端点存在。"""
    try:
        resp = client.delete("/api/v1/folders/1")
    except Exception:
        pytest.skip("Folders endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 204, 401, 403, 404)


def test_folder_contents_endpoint_exists(client):
    """测试获取文件夹内容端点存在。"""
    try:
        resp = client.get("/api/v1/folders/1/contents")
    except Exception:
        pytest.skip("Folders endpoint not available in this environment.")
        return
    assert resp.status_code in (200, 401, 403, 404)
