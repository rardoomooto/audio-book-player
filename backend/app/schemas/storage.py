from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class FileInfo:
    name: str
    path: str
    size: int
    mtime: float
    is_dir: bool


@dataclass
class FileMetadata:
    title: Optional[str] = None
    author: Optional[str] = None
    duration: Optional[float] = None
    format: Optional[str] = None
    cover: Optional[bytes] = None
