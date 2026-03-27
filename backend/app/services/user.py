import uuid
from datetime import datetime
from typing import Dict, List, Optional

from ..schemas.user import UserCreate, UserUpdate
from ..utils.user import hash_password, is_password_strong, verify_password


class UserService:
    """
    Lightweight in-memory user service with basic CRUD and password handling.
    This is a stand-in for a proper DB-backed implementation for the purposes
    of this exercise.
    """

    def __init__(self):
        # In-memory store: id -> user dict
        # Each user dict contains: id, username, email, password_hash, is_active, is_admin, created_at, updated_at
        self._users: Dict[int, Dict] = {}
        self._next_id: int = 1
        # Seed with a default admin for testing
        self._seed_admin()

    def _seed_admin(self):
        admin = {
            "id": self._next_id,
            "username": "admin",
            "email": "admin@example.com",
            "password_hash": hash_password("admin123"),
            "is_active": True,
            "is_admin": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        self._users[self._next_id] = admin
        self._next_id += 1

    # Helpers
    def _ensure_unique(self, username: str, email: str) -> None:
        for u in self._users.values():
            if u["username"] == username or u["email"] == email:
                raise ValueError("Username or email already exists")

    def get_users(self) -> List[Dict]:
        # Return sanitized dicts (exclude password_hash)
        return [self._sanitize(u) for u in self._users.values()]

    def get_user(self, user_id: int) -> Optional[Dict]:
        u = self._users.get(user_id)
        return self._sanitize(u) if u else None

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        for u in self._users.values():
            if u["username"] == username:
                return self._sanitize(u)
        return None

    def create_user(self, user_in: UserCreate) -> Dict:
        if not is_password_strong(user_in.password):
            raise ValueError("Password too weak")
        self._ensure_unique(user_in.username, user_in.email)
        user_id = self._next_id
        hashed = hash_password(user_in.password)
        now = datetime.utcnow()
        new = {
            "id": user_id,
            "username": user_in.username,
            "email": user_in.email,
            "password_hash": hashed,
            "is_active": True,
            "is_admin": user_in.is_admin,
            "created_at": now,
            "updated_at": now,
        }
        self._users[user_id] = new
        self._next_id += 1
        return self._sanitize(new)

    def update_user(self, user_id: int, user_update: UserUpdate) -> Dict:
        if user_id not in self._users:
            raise KeyError("User not found")
        u = self._users[user_id]
        if user_update.username is not None:
            # Ensure uniqueness
            for other in self._users.values():
                if other["id"] != user_id and other["username"] == user_update.username:
                    raise ValueError("Username already exists")
            u["username"] = user_update.username
        if user_update.email is not None:
            for other in self._users.values():
                if other["id"] != user_id and other["email"] == user_update.email:
                    raise ValueError("Email already exists")
            u["email"] = user_update.email
        if user_update.is_active is not None:
            u["is_active"] = user_update.is_active
        if user_update.is_admin is not None:
            u["is_admin"] = user_update.is_admin
        u["updated_at"] = datetime.utcnow()
        self._users[user_id] = u
        return self._sanitize(u)

    def delete_user(self, user_id: int) -> None:
        if user_id not in self._users:
            raise KeyError("User not found")
        del self._users[user_id]

    def set_password(self, user_id: int, password: str) -> None:
        if user_id not in self._users:
            raise KeyError("User not found")
        if not is_password_strong(password):
            raise ValueError("Password too weak")
        self._users[user_id]["password_hash"] = hash_password(password)
        self._users[user_id]["updated_at"] = datetime.utcnow()

    def set_status(self, user_id: int, is_active: bool) -> None:
        if user_id not in self._users:
            raise KeyError("User not found")
        self._users[user_id]["is_active"] = is_active
        self._users[user_id]["updated_at"] = datetime.utcnow()

    def _sanitize(self, u: Optional[Dict]) -> Optional[Dict]:
        if u is None:
            return None
        sanitized = {
            "id": u["id"],
            "username": u["username"],
            "email": u["email"],
            "full_name": None,
            "is_active": u.get("is_active", True),
            "is_admin": u.get("is_admin", False),
            "created_at": u.get("created_at", datetime.utcnow()),
            "updated_at": u.get("updated_at", datetime.utcnow()),
        }
        return sanitized


# Singleton instance for DI
_USER_SERVICE_INSTANCE: Optional[UserService] = None

def get_user_service() -> UserService:
    global _USER_SERVICE_INSTANCE
    if _USER_SERVICE_INSTANCE is None:
        _USER_SERVICE_INSTANCE = UserService()
    return _USER_SERVICE_INSTANCE

# Public alias for DI typing
user_service = get_user_service()
