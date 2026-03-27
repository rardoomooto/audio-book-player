from typing import List, Optional, Dict
from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field

# Services and dependencies
from ...services.content import (
    list_contents,
    get_content,
    create_content,
    update_content,
    delete_content,
    stream_url,
    scan_contents,
    search_contents,
)
from .deps import get_current_user

router = APIRouter()

class ContentBase(BaseModel):
    title: str
    author: Optional[str] = None
    album: Optional[str] = None
    duration_seconds: int = Field(..., ge=0)
    size_bytes: int = Field(..., ge=0)
    mime_type: str
    folder_id: Optional[int] = None
    metadata: dict = {}

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    album: Optional[str] = None
    duration_seconds: Optional[int] = None
    size_bytes: Optional[int] = None
    mime_type: Optional[str] = None
    folder_id: Optional[int] = None
    metadata: Optional[dict] = None

class Content(ContentBase):
    id: int
    created_at: str
    updated_at: str

# For compatibility with the new service, keep a minimal in-file mapping as fallback
contents_db_fallback: dict[int, Content] = {
    1: Content(id=1, title="Sample Track", author="Unknown Artist", album="Sample Album", duration_seconds=180, size_bytes=12345, mime_type="audio/mpeg", folder_id=None, metadata={}, created_at="2026-01-01", updated_at="2026-01-01"),
}
_fallback_next_id = 2


@router.get("/")
def list_contents_route(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    sort_by: str = Query("title", description="排序字段"),
    order: str = Query("asc", regex="^(asc|desc)$", description="排序顺序"),
    folder_id: Optional[int] = Query(None, description="文件夹ID"),
    search: Optional[str] = Query(None, description="通用搜索词"),
    author: Optional[str] = Query(None, description="作者筛选"),
    album: Optional[str] = Query(None, description="专辑筛选"),
    format: Optional[str] = Query(None, description="格式筛选"),
    min_duration: Optional[int] = Query(None, ge=0, description="最小时长（秒）"),
    max_duration: Optional[int] = Query(None, ge=0, description="最大时长（秒）"),
    current_user: Dict = Depends(get_current_user),
):
    """列出内容，支持多条件搜索和筛选。"""
    data = list_contents(
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        order=order,
        folder_id=folder_id,
        search=search,
        author=author,
        album=album,
        format=format,
        min_duration=min_duration,
        max_duration=max_duration,
    )
    items = [Content(**c) for c in data.get("items", [])]
    return {"total": data.get("total", 0), "items": items}


@router.get("/search")
def search_contents_route(
    q: str = Query(..., description="搜索查询"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    fields: Optional[List[str]] = Query(None, description="搜索字段列表"),
    current_user: Dict = Depends(get_current_user),
):
    """搜索内容。"""
    data = search_contents(
        query=q,
        page=page,
        page_size=page_size,
        fields=fields,
    )
    items = [Content(**c) for c in data.get("items", [])]
    return {"total": data.get("total", 0), "items": items}


@router.get("/{content_id}")
def get_content_route(content_id: int, current_user: Dict = Depends(get_current_user)) -> Content:
    content = get_content(content_id)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return Content(**content)


@router.post("/")
def create_content_route(content: ContentCreate, current_user: Dict = Depends(get_current_user)) -> Content:
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    data = content.dict()
    new = create_content(data)
    return Content(**new)


@router.put("/{content_id}")
def update_content_route(content_id: int, content: ContentUpdate, current_user: Dict = Depends(get_current_user)) -> Content:
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    updated = update_content(content_id, content.dict(exclude_unset=True))
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return Content(**updated)


@router.delete("/{content_id}")
def delete_content_route(content_id: int, current_user: Dict = Depends(get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    ok = delete_content(content_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return {"detail": "Deleted"}


@router.get("/{content_id}/stream")
def stream_content_route(content_id: int, current_user: Dict = Depends(get_current_user)) -> dict:
    # Permissions: if content exists, allow any user (admin or regular) to retrieve stream URL
    content = get_content(content_id)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return {"stream_url": stream_url(content_id)}


@router.post("/scan")
def scan_contents_route(current_user: Dict = Depends(get_current_user)) -> dict:
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return scan_contents()
