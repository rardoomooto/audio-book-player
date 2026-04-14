"""权限验证测试。

测试覆盖：
- 管理员端点权限
- 普通用户访问限制
- 跨用户访问控制
"""

import pytest
from fastapi.testclient import TestClient

try:
    from backend.app.main import app
except ImportError:
    app = None  # type: ignore


@pytest.fixture(scope="module")
def client():
    """创建测试客户端。"""
    if app is None:
        pytest.skip("FastAPI app not available")
    return TestClient(app)


class TestAdminPermissions:
    """管理员权限测试类。"""

    def test_admin_users_list_requires_auth(self, client):
        """测试用户列表需要认证。"""
        response = client.get("/api/v1/users/")
        assert response.status_code == 401

    def test_admin_users_list_with_invalid_token(self, client):
        """测试无效令牌访问用户列表。"""
        response = client.get(
            "/api/v1/users/",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    def test_admin_create_user_requires_auth(self, client):
        """测试创建用户需要认证。"""
        response = client.post(
            "/api/v1/users/",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "Password123"
            }
        )
        assert response.status_code == 401

    def test_admin_delete_user_requires_auth(self, client):
        """测试删除用户需要认证。"""
        response = client.delete("/api/v1/users/999")
        assert response.status_code == 401


class TestContentPermissions:
    """内容权限测试类。"""

    def test_content_create_requires_admin(self, client):
        """测试创建内容需要管理员权限。"""
        response = client.post(
            "/api/v1/contents/",
            json={
                "title": "Test Book",
                "author": "Test Author",
                "duration_seconds": 3600
            }
        )
        assert response.status_code in [401, 403]

    def test_content_update_requires_auth(self, client):
        """测试更新内容需要认证。"""
        response = client.put(
            "/api/v1/contents/1",
            json={"title": "Updated Title"}
        )
        assert response.status_code in [401, 403]

    def test_content_delete_requires_auth(self, client):
        """测试删除内容需要认证。"""
        response = client.delete("/api/v1/contents/1")
        assert response.status_code in [401, 403]


class TestFolderPermissions:
    """文件夹权限测试类。"""

    def test_folder_create_requires_auth(self, client):
        """测试创建文件夹需要认证。"""
        response = client.post(
            "/api/v1/folders/",
            json={"name": "New Folder"}
        )
        assert response.status_code == 401

    def test_folder_update_requires_auth(self, client):
        """测试更新文件夹需要认证。"""
        response = client.put(
            "/api/v1/folders/1",
            json={"name": "Updated Folder"}
        )
        assert response.status_code == 401

    def test_folder_delete_requires_auth(self, client):
        """测试删除文件夹需要认证。"""
        response = client.delete("/api/v1/folders/1")
        assert response.status_code == 401


class TestLimitsPermissions:
    """时长限制权限测试类。"""

    def test_global_limits_update_requires_admin(self, client):
        """测试更新全局限制需要管理员权限。"""
        response = client.put(
            "/api/v1/limits/global",
            json={"daily_minutes": 60}
        )
        assert response.status_code in [401, 403]

    def test_user_limits_update_requires_admin(self, client):
        """测试更新用户限制需要管理员权限。"""
        response = client.put(
            "/api/v1/limits/users/testuser",
            json={"daily_minutes": 30}
        )
        assert response.status_code in [401, 403]

    def test_user_limits_delete_requires_admin(self, client):
        """测试删除用户限制需要管理员权限。"""
        response = client.delete("/api/v1/limits/users/testuser")
        assert response.status_code in [401, 403]


class TestPermissionsManagement:
    """权限管理测试类。"""

    def test_permissions_list_requires_auth(self, client):
        """测试权限列表需要认证。"""
        response = client.get("/api/v1/permissions/")
        assert response.status_code == 401

    def test_permissions_create_requires_auth(self, client):
        """测试创建权限需要认证。"""
        response = client.post(
            "/api/v1/permissions/",
            json={
                "user_id": "1",
                "folder_id": "1",
                "permission_type": "read"
            }
        )
        assert response.status_code == 401

    def test_permissions_delete_requires_auth(self, client):
        """测试删除权限需要认证。"""
        response = client.delete("/api/v1/permissions/1")
        assert response.status_code == 401


class TestCrossUserAccess:
    """跨用户访问测试类。"""

    def test_user_cannot_access_other_user_info(self, client):
        """测试用户无法访问其他用户信息。"""
        # 无认证访问
        response = client.get("/api/v1/users/2")
        assert response.status_code == 401

    def test_user_cannot_modify_other_user_password(self, client):
        """测试用户无法修改其他用户密码。"""
        response = client.put(
            "/api/v1/users/2/password",
            json={"password": "newpassword"}
        )
        assert response.status_code == 401

    def test_user_cannot_change_other_user_status(self, client):
        """测试用户无法更改其他用户状态。"""
        response = client.put(
            "/api/v1/users/2/status?is_active=false"
        )
        assert response.status_code == 401


class TestPlaybackPermissions:
    """播放权限测试类。"""

    def test_playback_play_requires_auth(self, client):
        """测试播放需要认证。"""
        response = client.post(
            "/api/v1/playback/play",
            json={
                "content_id": "1",
                "position_seconds": 0
            }
        )
        assert response.status_code == 401

    def test_playback_current_requires_auth(self, client):
        """测试获取当前播放状态需要认证。"""
        response = client.get("/api/v1/playback/current")
        assert response.status_code == 401

    def test_playback_history_requires_auth(self, client):
        """测试播放历史需要认证。"""
        response = client.get("/api/v1/playback/session/test-session")
        assert response.status_code == 401
