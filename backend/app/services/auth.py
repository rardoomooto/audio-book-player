"""Authentication service (in-memory for prototype).

Provides simple user management and token generation helpers used by the
FastAPI endpoints.
"""

from __future__ import annotations

from typing import Optional, Dict
from datetime import timedelta

from ..core.security import get_password_hash, verify_password, create_access_token
from .token_blacklist import blacklist_token  # for potential cross-use
from ..core.config import get_settings

_settings = get_settings()

# In-memory user store (could be replaced with real DB later)
_USERS: Dict[str, Dict] = {}


def _ensure_default_users() -> None:
    if not _USERS:
        # Create a default admin user with password 'admin'
        admin_username = "admin"
        admin = {
            "username": admin_username,
            "email": "admin@example.com",
            "password_hash": get_password_hash("admin"),
            "is_active": True,
            "is_admin": True,
        }
        _USERS[admin_username] = admin


def get_user_by_username(username: str) -> Optional[Dict]:
    _ensure_default_users()
    return _USERS.get(username)


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    user = get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return user


def create_token_pair(user: Dict) -> Dict:
    """Create access and refresh tokens for a given user."""
    # Access token: 15 minutes by default
    access_token = create_access_token({"sub": user["username"], "type": "access"}, timedelta(minutes=15))
    # Refresh token: 7 days
    refresh_token = create_access_token({"sub": user["username"], "type": "refresh"}, timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 15 * 60,
    }
