"""安全工具单元测试。"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from jose import jwt, JWTError
from backend.app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    pwd_context,
)
from backend.app.core.config import get_settings


class TestPasswordHashing:
    """密码哈希测试。"""

    def test_get_password_hash(self):
        """测试生成密码哈希。"""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")

    def test_verify_password_correct(self):
        """测试验证正确密码。"""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """测试验证错误密码。"""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False

    def test_different_passwords_different_hashes(self):
        """测试不同密码产生不同哈希。"""
        hash1 = get_password_hash("Password1")
        hash2 = get_password_hash("Password2")
        
        assert hash1 != hash2

    def test_same_password_different_hashes(self):
        """测试相同密码产生不同哈希（因为salt）。"""
        password = "SamePassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # bcrypt每次生成不同的salt，所以哈希不同
        assert hash1 != hash2
        # 但都能验证
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestCreateAccessToken:
    """JWT访问令牌创建测试。"""

    def test_create_access_token_default_expiry(self):
        """测试使用默认过期时间创建令牌。"""
        data = {"sub": "testuser", "type": "access"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_custom_expiry(self):
        """测试使用自定义过期时间创建令牌。"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta=expires_delta)
        
        settings = get_settings()
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        
        assert "exp" in payload
        assert payload["sub"] == "testuser"

    def test_create_access_token_contains_jti(self):
        """测试创建的令牌包含JTI。"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        settings = get_settings()
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        
        assert "jti" in payload
        assert len(payload["jti"]) > 0

    def test_create_access_token_unique_jti(self):
        """测试每次创建的令牌有唯一的JTI。"""
        data = {"sub": "testuser"}
        token1 = create_access_token(data)
        token2 = create_access_token(data)
        
        settings = get_settings()
        payload1 = jwt.decode(token1, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        payload2 = jwt.decode(token2, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        
        assert payload1["jti"] != payload2["jti"]

    def test_create_access_token_preserves_data(self):
        """测试创建的令牌保留原始数据。"""
        data = {"sub": "testuser", "type": "access", "role": "admin"}
        token = create_access_token(data)
        
        settings = get_settings()
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        
        assert payload["sub"] == "testuser"
        assert payload["type"] == "access"
        assert payload["role"] == "admin"

    @patch('backend.app.services.token_blacklist.blacklist_token')
    def test_create_access_token_registers_in_blacklist(self, mock_blacklist):
        """测试创建的令牌注册到黑名单。"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        # 应该调用blacklist_token来注册JTI
        mock_blacklist.assert_called_once()


class TestGetCurrentUser:
    """获取当前用户测试。"""

    @pytest.fixture
    def valid_token(self):
        """创建有效的访问令牌。"""
        data = {"sub": "admin", "type": "access"}
        return create_access_token(data)

    @patch('backend.app.core.security.get_user_by_username')
    @patch('backend.app.core.security.is_token_blacklisted')
    def test_get_current_user_valid(self, mock_blacklisted, mock_get_user, valid_token):
        """测试使用有效令牌获取用户。"""
        mock_blacklisted.return_value = False
        mock_get_user.return_value = {
            "username": "admin",
            "email": "admin@example.com",
            "is_active": True,
            "is_admin": True,
        }
        
        import asyncio
        user = asyncio.run(get_current_user(valid_token))
        
        assert user["username"] == "admin"

    def test_get_current_user_invalid_token(self):
        """测试使用无效令牌。"""
        import asyncio
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(get_current_user("invalid_token"))
        
        assert exc_info.value.status_code == 401

    @patch('backend.app.core.security.is_token_blacklisted')
    def test_get_current_user_blacklisted_token(self, mock_blacklisted, valid_token):
        """测试使用已列入黑名单的令牌。"""
        mock_blacklisted.return_value = True
        
        import asyncio
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(get_current_user(valid_token))
        
        assert exc_info.value.status_code == 401

    @patch('backend.app.core.security.get_user_by_username')
    @patch('backend.app.core.security.is_token_blacklisted')
    def test_get_current_user_user_not_found(self, mock_blacklisted, mock_get_user, valid_token):
        """测试用户不存在时获取用户。"""
        mock_blacklisted.return_value = False
        mock_get_user.return_value = None
        
        import asyncio
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(get_current_user(valid_token))
        
        assert exc_info.value.status_code == 401

    def test_get_current_user_no_sub_claim(self):
        """测试令牌没有sub声明。"""
        settings = get_settings()
        token = jwt.encode(
            {"type": "access", "exp": datetime.utcnow() + timedelta(minutes=15)},
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )
        
        import asyncio
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(get_current_user(token))
        
        assert exc_info.value.status_code == 401
