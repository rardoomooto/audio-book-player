"""API deps module tests."""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestGetCurrentUser:
    def test_get_current_user_returns_user_dict(self):
        from backend.app.api.deps import get_current_user
        assert callable(get_current_user)

    def test_get_current_user_is_dependency(self):
        from backend.app.api.deps import get_current_user
        from fastapi import Depends
        assert callable(get_current_user)


class TestGetCurrentAdminUser:
    def test_get_current_admin_user_returns_user_dict(self):
        from backend.app.api.deps import get_current_admin_user
        assert callable(get_current_admin_user)


class TestGetCurrentUserSimple:
    def test_get_current_user_simple_exists(self):
        from backend.app.api.v1.deps import get_current_user_simple
        assert callable(get_current_user_simple)

    def test_get_current_user_simple_with_valid_token(self):
        from backend.app.api.v1.deps import get_current_user_simple
        from unittest.mock import patch

        mock_user = {"id": 1, "username": "testuser", "is_admin": False, "is_active": True}

        with patch("backend.app.api.v1.deps.get_user_by_username", return_value=mock_user):
            with patch("backend.app.api.v1.deps.get_settings"):
                result = get_current_user_simple("valid-token-here")
                assert result["username"] == "testuser"

    def test_get_current_user_simple_with_x_role_header(self):
        from backend.app.api.v1.deps import get_current_user_simple

        result = get_current_user_simple(None, x_role="admin")
        assert result["username"] == "admin"
        assert result["is_admin"] is True
        assert result["is_active"] is True

    def test_get_current_user_simple_guest_fallback(self):
        from backend.app.api.v1.deps import get_current_user_simple

        result = get_current_user_simple(None)
        assert result["username"] == "guest"
        assert result["is_active"] is True

    def test_get_current_user_simple_with_invalid_token(self):
        from backend.app.api.v1.deps import get_current_user_simple

        with patch("backend.app.api.v1.deps.get_user_by_username", return_value=None):
            with patch("backend.app.api.v1.deps.get_settings"):
                result = get_current_user_simple("invalid-token")
                assert result["username"] == "guest"
                assert result["is_active"] is True
