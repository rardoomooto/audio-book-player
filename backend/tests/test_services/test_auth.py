"""认证服务单元测试。"""

import pytest
from unittest.mock import patch, MagicMock
from backend.app.services.auth import (
    get_user_by_username,
    authenticate_user,
    create_token_pair,
    _ensure_default_users,
    _USERS,
)


class TestAuthService:
    """认证服务测试。"""

    @pytest.fixture(autouse=True)
    def clear_users(self):
        """每个测试前清空用户存储。"""
        _USERS.clear()
        yield
        _USERS.clear()

    def test_ensure_default_users_creates_admin(self):
        """测试创建默认管理员用户。"""
        _ensure_default_users()
        
        assert "admin" in _USERS
        admin = _USERS["admin"]
        assert admin["username"] == "admin"
        assert admin["email"] == "admin@example.com"
        assert admin["is_active"] is True
        assert admin["is_admin"] is True
        assert "password_hash" in admin

    def test_ensure_default_users_idempotent(self):
        """测试多次调用不会重复创建用户。"""
        _ensure_default_users()
        _ensure_default_users()
        
        assert len(_USERS) == 1

    def test_get_user_by_username_existing(self):
        """测试获取存在的用户。"""
        _ensure_default_users()
        
        user = get_user_by_username("admin")
        assert user is not None
        assert user["username"] == "admin"

    def test_get_user_by_username_nonexistent(self):
        """测试获取不存在的用户。"""
        user = get_user_by_username("nonexistent")
        assert user is None

    def test_authenticate_user_valid_credentials(self):
        """测试使用有效凭据认证。"""
        _ensure_default_users()
        
        user = authenticate_user("admin", "admin")
        assert user is not None
        assert user["username"] == "admin"

    def test_authenticate_user_invalid_username(self):
        """测试使用无效用户名认证。"""
        user = authenticate_user("nonexistent", "admin")
        assert user is None

    def test_authenticate_user_invalid_password(self):
        """测试使用无效密码认证。"""
        _ensure_default_users()
        
        user = authenticate_user("admin", "wrongpassword")
        assert user is None

    def test_create_token_pair(self):
        """测试创建令牌对。"""
        _ensure_default_users()
        user = _USERS["admin"]
        
        tokens = create_token_pair(user)
        
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert "token_type" in tokens
        assert tokens["token_type"] == "bearer"
        assert "expires_in" in tokens
        assert tokens["expires_in"] == 15 * 60  # 15分钟

    def test_create_token_pair_contains_jwt(self):
        """测试创建的令牌是有效的JWT格式。"""
        _ensure_default_users()
        user = _USERS["admin"]
        
        tokens = create_token_pair(user)
        
        # JWT令牌应该以eyJ开头（Base64编码的header）
        assert tokens["access_token"].startswith("eyJ")
        assert tokens["refresh_token"].startswith("eyJ")

    @patch('backend.app.services.auth.create_access_token')
    def test_create_token_pair_calls_create_access_token(self, mock_create_token):
        """测试create_token_pair正确调用create_access_token。"""
        mock_create_token.return_value = "mock_token"
        
        user = {"username": "testuser"}
        tokens = create_token_pair(user)
        
        # 应该调用两次：一次用于access token，一次用于refresh token
        assert mock_create_token.call_count == 2
        
        # 验证调用参数
        calls = mock_create_token.call_args_list
        assert calls[0][0][0] == {"sub": "testuser", "type": "access"}
        assert calls[1][0][0] == {"sub": "testuser", "type": "refresh"}


class TestAuthServiceIntegration:
    """认证服务集成测试。"""

    @pytest.fixture(autouse=True)
    def clear_users(self):
        """每个测试前清空用户存储。"""
        _USERS.clear()
        yield
        _USERS.clear()

    def test_full_authentication_flow(self):
        """测试完整的认证流程。"""
        # 1. 确保默认用户存在
        _ensure_default_users()
        
        # 2. 使用有效凭据认证
        user = authenticate_user("admin", "admin")
        assert user is not None
        
        # 3. 创建令牌对
        tokens = create_token_pair(user)
        assert tokens["access_token"] is not None
        assert tokens["refresh_token"] is not None
