"""Security utilities and OAuth2 helpers with real JWT support.

This module provides password hashing helpers, JWT creation/validation,
and a lightweight integration point for an in-memory user store used by
the authentication services.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4
from passlib.context import CryptContext
from ..services.auth import get_user_by_username
from ..services.token_blacklist import is_token_blacklisted

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status

from ..core.config import Settings
from ..core.config import get_settings

settings = get_settings()

# OAuth2 scheme for token retrieval
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Password hashing utilities (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    to_encode.update({"exp": expire})
    # Always assign a unique token identifier (JTI) for potential blacklist rotation
    jti = str(uuid4())
    to_encode.update({"jti": jti})
    token = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    # Register token in a lightweight blacklist store (for logout/rotation)
    try:
        from ..services.token_blacklist import blacklist_token
        blacklist_token(to_encode["jti"], int(expire.timestamp()))
    except Exception:
        pass
    return token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Blacklist check
        jti = payload.get("jti")
        if jti and is_token_blacklisted(jti):
            raise credentials_exception
        user = get_user_by_username(username)
        if not user:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
