from typing import Optional, Dict
from fastapi import Header, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# Lightweight dependency to determine current user role for permissions.
# This is a simplified version - the real authentication is in backend.app.api.deps
async def get_current_user_simple(
    authorization: Optional[str] = Header(None),
    x_role: Optional[str] = Header(None),
    token: Optional[str] = Depends(oauth2_scheme)
) -> Dict[str, object]:
    """
    Simple user dependency for basic authentication.
    For full authentication flow, use get_current_user from backend.app.api.deps
    """
    # Import here to avoid circular dependencies
    from ..services.auth import get_user_by_username
    from jose import jwt, JWTError
    from ..core.config import get_settings
    
    settings = get_settings()
    
    # Try OAuth2 token first
    if token:
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            username: Optional[str] = payload.get("sub")
            if username:
                user = get_user_by_username(username)
                if user:
                    return {
                        "username": user["username"],
                        "email": user.get("email", ""),
                        "is_admin": bool(user.get("is_admin", False)),
                        "is_active": bool(user.get("is_active", True)),
                    }
        except JWTError:
            pass
    
    # Try Bearer token from Authorization header
    if authorization and authorization.startswith("Bearer "):
        token_str = authorization.split(" ")[1]
        try:
            payload = jwt.decode(token_str, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            username: Optional[str] = payload.get("sub")
            if username:
                user = get_user_by_username(username)
                if user:
                    return {
                        "username": user["username"],
                        "email": user.get("email", ""),
                        "is_admin": bool(user.get("is_admin", False)),
                        "is_active": bool(user.get("is_active", True)),
                    }
        except JWTError:
            pass
    
    # Fallback to role header for simplicity
    if x_role:
        is_admin = x_role.lower() == "admin"
        return {"username": x_role, "email": "", "is_admin": is_admin, "is_active": True}
    
    # Public guest user
    return {"username": "guest", "email": "", "is_admin": False, "is_active": True}
