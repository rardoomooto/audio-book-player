from datetime import datetime
from typing import List, Optional, Dict, Any

# In-memory store for demo purposes. This mimics a lightweight data layer.
_contents: Dict[int, Dict] = {
    1: {
        "id": 1,
        "title": "Sample Track",
        "author": "Unknown Artist",
        "album": "Sample Album",
        "duration_seconds": 180,
        "size_bytes": 12345,
        "mime_type": "audio/mpeg",
        "folder_id": None,
        "content_metadata": {},
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
}
_next_id = 2


def _now_iso() -> str:
    return datetime.utcnow().isoformat()


def list_contents(
    page: int = 1,
    page_size: int = 20,
    sort_by: str = "title",
    order: str = "asc",
    folder_id: Optional[int] = None,
    search: Optional[str] = None,
    author: Optional[str] = None,
    album: Optional[str] = None,
    format: Optional[str] = None,
    min_duration: Optional[int] = None,
    max_duration: Optional[int] = None,
) -> Dict[str, object]:
    """列出内容，支持多条件搜索和筛选。
    
    Args:
        page: 页码
        page_size: 每页大小
        sort_by: 排序字段
        order: 排序顺序 (asc/desc)
        folder_id: 文件夹ID
        search: 通用搜索词（搜索标题、作者、专辑）
        author: 作者筛选
        album: 专辑筛选
        format: 格式筛选
        min_duration: 最小时长（秒）
        max_duration: 最大时长（秒）
        
    Returns:
        Dict[str, object]: 包含total和items的字典
    """
    items = list(_contents.values())
    
    # 文件夹筛选
    if folder_id is not None:
        items = [c for c in items if c.get("folder_id") == folder_id]
    
    # 通用搜索
    if search:
        q = search.lower()
        items = [
            c for c in items
            if q in c.get("title", "").lower()
            or q in c.get("author", "").lower()
            or q in c.get("album", "").lower()
        ]
    
    # 作者筛选
    if author:
        author_lower = author.lower()
        items = [c for c in items if author_lower in c.get("author", "").lower()]
    
    # 专辑筛选
    if album:
        album_lower = album.lower()
        items = [c for c in items if album_lower in c.get("album", "").lower()]
    
    # 格式筛选
    if format:
        format_lower = format.lower()
        items = [c for c in items if format_lower in c.get("mime_type", "").lower()]
    
    # 时长筛选
    if min_duration is not None:
        items = [c for c in items if c.get("duration_seconds", 0) >= min_duration]
    if max_duration is not None:
        items = [c for c in items if c.get("duration_seconds", 0) <= max_duration]
    
    # 排序 - 使用安全的key函数处理None值
    reverse = (order or "asc").lower() == "desc"
    def sort_key(x: Dict) -> Any:
        val = x.get(sort_by)
        # 对None值和字符串进行安全排序
        if val is None:
            return ""
        return val
    items.sort(key=sort_key, reverse=reverse)
    
    # 分页
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    paged = items[start:end]
    
    return {"total": total, "items": paged}


def search_contents(
    query: str,
    page: int = 1,
    page_size: int = 20,
    fields: Optional[List[str]] = None,
) -> Dict[str, object]:
    """搜索内容。
    
    Args:
        query: 搜索查询
        page: 页码
        page_size: 每页大小
        fields: 搜索字段列表，默认为标题、作者、专辑
        
    Returns:
        Dict[str, object]: 包含total和items的字典
    """
    if not fields:
        fields = ["title", "author", "album"]
    
    query_lower = query.lower()
    items = list(_contents.values())
    
    # 在指定字段中搜索
    matched_items = []
    for item in items:
        for field in fields:
            field_value = str(item.get(field, "")).lower()
            if query_lower in field_value:
                matched_items.append(item)
                break
    
    # 分页
    total = len(matched_items)
    start = (page - 1) * page_size
    end = start + page_size
    paged = matched_items[start:end]
    
    return {"total": total, "items": paged}


def get_content(content_id: int) -> Optional[Dict]:
    return _contents.get(content_id)


def create_content(data: Dict) -> Dict:
    global _next_id
    now = _now_iso()
    new = {
        "id": _next_id,
        "title": data.get("title"),
        "duration_seconds": data.get("duration_seconds", 0),
        "size_bytes": data.get("size_bytes", 0),
        "mime_type": data.get("mime_type", "audio/mpeg"),
        "folder_id": data.get("folder_id"),
        "content_metadata": data.get("content_metadata", {}),
        "created_at": now,
        "updated_at": now,
    }
    _contents[_next_id] = new
    _next_id += 1
    return new


def update_content(content_id: int, data: Dict) -> Optional[Dict]:
    if content_id not in _contents:
        return None
    c = _contents[content_id]
    if "title" in data:
        c["title"] = data["title"]
    if "duration_seconds" in data:
        c["duration_seconds"] = data["duration_seconds"]
    if "size_bytes" in data:
        c["size_bytes"] = data["size_bytes"]
    if "mime_type" in data:
        c["mime_type"] = data["mime_type"]
    if "folder_id" in data:
        c["folder_id"] = data["folder_id"]
    if "content_metadata" in data:
        c["content_metadata"] = data["content_metadata"]
    c["updated_at"] = _now_iso()
    _contents[content_id] = c
    return c


def delete_content(content_id: int) -> bool:
    if content_id in _contents:
        del _contents[content_id]
        return True
    return False


def stream_url(content_id: int) -> Optional[str]:
    if content_id not in _contents:
        return None
    return f"https://stream.local/content/{content_id}"


def scan_contents() -> Dict[str, object]:
    # Placeholder: pretend we scanned NAS and found existing contents
    return {"scanned": True, "count": len(_contents)}
