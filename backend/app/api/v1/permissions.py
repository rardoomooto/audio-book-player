from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Permission(BaseModel):
    id: int
    name: str
    description: str | None = None
    level: str


class PermissionCreate(BaseModel):
    name: str
    description: str | None = None
    level: str


_permissions: List[Permission] = [Permission(id=1, name="view_content", description=None, level="read")]


@router.get("/")
def list_permissions() -> List[Permission]:
    return _permissions


@router.post("/")
def create_permission(p: PermissionCreate) -> Permission:
    new_id = max([perm.id for perm in _permissions], default=0) + 1
    perm = Permission(id=new_id, name=p.name, description=p.description, level=p.level)
    _permissions.append(perm)
    return perm


@router.delete("/{permission_id}")
def delete_permission(permission_id: int):
    global _permissions
    _permissions = [p for p in _permissions if p.id != permission_id]
    return {"detail": "Deleted"}


@router.get("/users/{user_id}")
def user_permissions(user_id: int) -> List[Permission]:
    # Placeholder: return all permissions for a user
    return _permissions


@router.put("/users/{user_id}")
def update_user_permissions(user_id: int):
    return {"detail": f"Permissions updated for user {user_id}"}
