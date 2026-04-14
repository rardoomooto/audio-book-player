from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm

from ...services.auth import authenticate_user, create_token_pair, get_user_by_username
from ...api.deps import get_current_active_user, get_current_admin_user
from ...core.config import get_settings
from ...core.security import oauth2_scheme
from ...core.security import create_access_token
from ...schemas.token import TokenPair as TokenPairModel
from ...schemas.token import Token as TokenModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str


class UserMe(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool


@router.post("/login", response_model=TokenPairModel)
def login(req: LoginRequest):
    user = authenticate_user(req.username, req.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token_pair = create_token_pair(user)
    return TokenPairModel(**token_pair)


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=TokenModel)
def refresh(req: RefreshRequest):
    if not req.refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    try:
        from jose import jwt
        settings = get_settings()
        payload = jwt.decode(req.refresh_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        username: str = payload.get("sub") or ""
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        user = get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
        # Issue new access token
        new_access = create_access_token({"sub": username, "type": "access"}, timedelta(minutes=15))
        return TokenModel(access_token=new_access, expires_in=15 * 60, token_type="bearer")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


@router.post("/logout")
def logout(token: Optional[str] = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    # Decode to extract jti and blacklist it
    from jose import jwt
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        jti = payload.get("jti")
        if jti:
            from ...services.token_blacklist import blacklist_token
            exp_ts = payload.get("exp")
            exp_timestamp = int(exp_ts.timestamp()) if hasattr(exp_ts, 'timestamp') else int(exp_ts) if exp_ts else 0
            blacklist_token(jti, exp_timestamp)
    except JWTError:
        pass
    return {"detail": "Logged out"}


@router.get("/me", response_model=UserMe)
def me(current_user: dict = Depends(get_current_active_user)):
    # current_user is provided by dependency as a user dict; map to response model
    return UserMe(
        username=current_user["username"],
        email=current_user["email"],
        is_active=current_user["is_active"],
        is_admin=current_user["is_admin"],
    )
