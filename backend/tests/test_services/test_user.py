"""用户服务单元测试。"""

import pytest
from datetime import datetime
from backend.app.services.user import UserService, get_user_service, _USER_SERVICE_INSTANCE
from backend.app.schemas.user import UserCreate, UserUpdate


class TestUserService:
    """用户服务测试。"""

    @pytest.fixture
    def service(self):
        """创建用户服务实例。"""
        svc = UserService()
        return svc

    def test_init_creates_admin(self, service):
        """测试初始化时创建管理员用户。"""
        users = service.get_users()
        assert len(users) == 1
        assert users[0]["username"] == "admin"
        assert users[0]["is_admin"] is True

    def test_get_users_returns_sanitized(self, service):
        """测试get_users返回脱敏数据。"""
        users = service.get_users()
        for user in users:
            assert "password_hash" not in user
            assert "id" in user
            assert "username" in user

    def test_get_user_existing(self, service):
        """测试获取存在的用户。"""
        user = service.get_user(1)
        assert user is not None
        assert user["username"] == "admin"
        assert "password_hash" not in user

    def test_get_user_nonexistent(self, service):
        """测试获取不存在的用户。"""
        user = service.get_user(999)
        assert user is None

    def test_get_user_by_username_existing(self, service):
        """测试通过用户名获取用户。"""
        user = service.get_user_by_username("admin")
        assert user is not None
        assert user["username"] == "admin"

    def test_get_user_by_username_nonexistent(self, service):
        """测试通过用户名获取不存在的用户。"""
        user = service.get_user_by_username("nonexistent")
        assert user is None

    def test_create_user_success(self, service):
        """测试成功创建用户。"""
        user_in = UserCreate(
            username="testuser",
            email="test@example.com",
            password="StrongPass123!",
            is_admin=False,
        )
        user = service.create_user(user_in)
        
        assert user["username"] == "testuser"
        assert user["email"] == "test@example.com"
        assert user["is_admin"] is False
        assert user["is_active"] is True
        assert "password_hash" not in user

    def test_create_user_weak_password(self, service):
        """测试使用弱密码创建用户。"""
        user_in = UserCreate(
            username="testuser",
            email="test@example.com",
            password="weak",
            is_admin=False,
        )
        with pytest.raises(ValueError, match="Password too weak"):
            service.create_user(user_in)

    def test_create_user_duplicate_username(self, service):
        """测试创建重复用户名的用户。"""
        user_in = UserCreate(
            username="admin",
            email="new@example.com",
            password="StrongPass123!",
            is_admin=False,
        )
        with pytest.raises(ValueError, match="Username or email already exists"):
            service.create_user(user_in)

    def test_create_user_duplicate_email(self, service):
        """测试创建重复邮箱的用户。"""
        user_in = UserCreate(
            username="newuser",
            email="admin@example.com",
            password="StrongPass123!",
            is_admin=False,
        )
        with pytest.raises(ValueError, match="Username or email already exists"):
            service.create_user(user_in)

    def test_update_user_username(self, service):
        """测试更新用户名。"""
        update = UserUpdate(username="newadmin")
        user = service.update_user(1, update)
        
        assert user["username"] == "newadmin"

    def test_update_user_email(self, service):
        """测试更新邮箱。"""
        update = UserUpdate(email="newadmin@example.com")
        user = service.update_user(1, update)
        
        assert user["email"] == "newadmin@example.com"

    def test_update_user_is_active(self, service):
        """测试更新用户状态。"""
        update = UserUpdate(is_active=False)
        user = service.update_user(1, update)
        
        assert user["is_active"] is False

    def test_update_user_nonexistent(self, service):
        """测试更新不存在的用户。"""
        update = UserUpdate(username="newname")
        with pytest.raises(KeyError, match="User not found"):
            service.update_user(999, update)

    def test_update_user_duplicate_username(self, service):
        """测试更新为重复的用户名。"""
        user_in = UserCreate(
            username="testuser",
            email="test@example.com",
            password="StrongPass123!",
            is_admin=False,
        )
        service.create_user(user_in)
        
        update = UserUpdate(username="testuser")
        with pytest.raises(ValueError, match="Username already exists"):
            service.update_user(1, update)

    def test_delete_user_success(self, service):
        """测试成功删除用户。"""
        user_in = UserCreate(
            username="testuser",
            email="test@example.com",
            password="StrongPass123!",
            is_admin=False,
        )
        created = service.create_user(user_in)
        user_id = created["id"]
        
        service.delete_user(user_id)
        
        assert service.get_user(user_id) is None

    def test_delete_user_nonexistent(self, service):
        """测试删除不存在的用户。"""
        with pytest.raises(KeyError, match="User not found"):
            service.delete_user(999)

    def test_set_password_success(self, service):
        """测试成功设置密码。"""
        service.set_password(1, "NewStrongPass123!")
        
        user = service.get_user(1)
        assert user is not None

    def test_set_password_weak(self, service):
        """测试设置弱密码。"""
        with pytest.raises(ValueError, match="Password too weak"):
            service.set_password(1, "weak")

    def test_set_password_nonexistent_user(self, service):
        """测试为不存在的用户设置密码。"""
        with pytest.raises(KeyError, match="User not found"):
            service.set_password(999, "NewStrongPass123!")

    def test_set_status_success(self, service):
        """测试成功设置用户状态。"""
        service.set_status(1, False)
        
        user = service.get_user(1)
        assert user["is_active"] is False

    def test_set_status_nonexistent_user(self, service):
        """测试为不存在的用户设置状态。"""
        with pytest.raises(KeyError, match="User not found"):
            service.set_status(999, False)


class TestGetUserService:
    """get_user_service函数测试。"""

    def test_returns_singleton(self):
        """测试返回单例实例。"""
        global _USER_SERVICE_INSTANCE
        _USER_SERVICE_INSTANCE = None
        
        svc1 = get_user_service()
        svc2 = get_user_service()
        
        assert svc1 is svc2
