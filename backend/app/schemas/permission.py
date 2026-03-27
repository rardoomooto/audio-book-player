from typing import Optional, List
from pydantic import BaseModel


class Permission(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    level: str


class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    level: str
