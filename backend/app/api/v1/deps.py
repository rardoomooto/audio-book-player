from typing import Optional, Dict
from fastapi import Header


# Lightweight dependency to determine current user role for permissions.
def get_current_user(authorization: Optional[str] = Header(None), x_role: Optional[str] = Header(None)) -> Dict[str, object]:
    # Try Bearer token from Authorization header
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        try:
            from backend.app.api.v1.auth import tokens_store, fake_users_db  # lazy import to avoid cycles
            username = tokens_store.get(token)
            if username:
                user = fake_users_db.get(username)
                if user:
                    return {
                        "username": user["username"],
                        "is_admin": bool(user.get("is_admin", False)),
                    }
        except Exception:
            pass
    # Fallback to role header for simplicity
    if x_role:
        is_admin = x_role.lower() == "admin"
        return {"username": x_role, "is_admin": is_admin}
    # Public guest user
    return {"username": "guest", "is_admin": False}
