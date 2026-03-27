from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

from backend.app.api.deps import get_current_admin
from backend.app.schemas.user import User, UserCreate, UserUpdate
from backend.app.services.user import get_user_service
from backend.app.core.config import get_settings
from backend.app.utils.user import verify_password

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
settings = get_settings()


class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool = False


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class UserUpdateIn(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class PasswordUpdate(BaseModel):
    password: str


async def _get_current_user_with_role(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub") or payload.get("username") or payload.get("user")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        svc = get_user_service()
        user = svc.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return {"id": user["id"], "username": user["username"], "is_admin": user["is_admin"]}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def _admin_required(current: dict = Depends(_get_current_user_with_role)):
    if not current.get("is_admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current


@router.get("/")
def list_users(current_admin: dict = Depends(_admin_required)):
    svc = get_user_service()
    users = svc.get_users()
    return [UserOut(**{
        "id": u["id"],
        "username": u["username"],
        "email": u["email"],
        "is_active": u["is_active"],
        "is_admin": u["is_admin"],
        "created_at": u["created_at"],
        "updated_at": u["updated_at"],
    }) for u in users]


@router.post("/")
def create_user(user_in: UserIn, current_admin: dict = Depends(_admin_required)):
    svc = get_user_service()
    created = svc.create_user(UserCreate(
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        is_admin=user_in.is_admin,
    ))
    return UserOut(**created, created_at=created.get("created_at"), updated_at=created.get("updated_at"))


@router.get("/{user_id}")
def get_user(user_id: int, current_user: dict = Depends(_get_current_user_with_role)):
    # Admin can view any user; non-admin can view only themselves
    if not current_user.get("is_admin") and current_user.get("id") != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this user")
    svc = get_user_service()
    user = svc.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut(**user)


@router.put("/{user_id}")
def update_user(user_id: int, user_update: UserUpdateIn, current_user: dict = Depends(_get_current_user_with_role)):
    if (not current_user.get("is_admin")) and (current_user.get("id") != user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")
    svc = get_user_service()
    updated = svc.update_user(user_id, UserUpdate(
        username=user_update.username,
        email=user_update.email,
        is_active=user_update.is_active,
        is_admin=user_update.is_admin,
    ))
    return UserOut(**updated)


@router.delete("/{user_id}")
def delete_user(user_id: int, current_admin: dict = Depends(_admin_required)):
    svc = get_user_service()
    try:
        svc.delete_user(user_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"detail": "Deleted"}


@router.put("/{user_id}/password")
def change_password(user_id: int, payload: PasswordUpdate, current_user: dict = Depends(_get_current_user_with_role)):
    if (not current_user.get("is_admin")) and (current_user.get("id") != user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to change this password")
    svc = get_user_service()
    if not payload.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password required")
    try:
        svc.set_password(user_id, payload.password)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    return {"detail": "Password updated"}


@router.put("/{user_id}/status")
def update_status(user_id: int, is_active: bool, current_admin: dict = Depends(_admin_required)):
    svc = get_user_service()
    try:
        svc.set_status(user_id, is_active)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"detail": "Status updated"}
