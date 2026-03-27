from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class ContentBase(BaseModel):
    title: str
    duration_seconds: int
    size_bytes: int
    mime_type: str
    folder_id: Optional[int] = None
    content_metadata: Dict[str, Any] = {}


class ContentCreate(ContentBase):
    pass


class ContentUpdate(BaseModel):
    title: Optional[str] = None
    duration_seconds: Optional[int] = None
    size_bytes: Optional[int] = None
    mime_type: Optional[str] = None
    folder_id: Optional[int] = None
    content_metadata: Optional[Dict[str, Any]] = None


class Content(ContentBase):
    id: int
    created_at: datetime
    updated_at: datetime


class Folder(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
