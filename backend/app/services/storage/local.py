from __future__ import annotations

import io
import os
from pathlib import Path
from typing import List, Optional

from mutagen import File as MutagenFile

from .base import StorageBase
from ...schemas.storage import FileInfo, FileMetadata
from ...utils.storage import extract_metadata_from_bytes
from ...utils.storage_errors import (
    StorageFileNotFoundError,
    StoragePermissionError,
    handle_storage_exception,
)


class LocalStorage(StorageBase):
    """Local filesystem storage backend supporting mounted paths."""

    def __init__(self, mount_path: Optional[str] = None):
        # If no mount path is provided, default to current working dir
        self.mount_path = Path(mount_path or ".").resolve()

    def _abs_path(self, path: str) -> Path:
        p = Path(path)
        if not p.is_absolute():
            p = self.mount_path / p
        return p

    def list_files(self, path: str) -> List[FileInfo]:
        base = self._abs_path(path)
        items: List[FileInfo] = []
        if not base.exists():
            return items
        
        try:
            for entry in base.iterdir():
                try:
                    stat = entry.stat()
                    items.append(
                        FileInfo(
                            name=entry.name,
                            path=str(entry.resolve()),
                            size=stat.st_size,
                            mtime=stat.st_mtime,
                            is_dir=entry.is_dir(),
                        )
                    )
                except PermissionError:
                    # 跳过权限不足的文件，但继续处理其他文件
                    continue
                except Exception as e:
                    # 记录警告但继续处理
                    continue
        except PermissionError as e:
            raise StoragePermissionError(path, "列出目录")
        except Exception as e:
            raise handle_storage_exception(e, "list_files", path)
        
        return items

    def read_file(self, path: str) -> bytes:
        p = self._abs_path(path)
        try:
            with open(p, "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise StorageFileNotFoundError(path)
        except PermissionError:
            raise StoragePermissionError(path, "读取")
        except Exception as e:
            raise handle_storage_exception(e, "read_file", path)

    def get_metadata(self, path: str) -> FileMetadata:
        try:
            data = self.read_file(path)
            return extract_metadata_from_bytes(data, path)
        except Exception as e:
            # 如果是已知的存储异常，直接抛出
            if "Storage" in type(e).__name__:
                raise
            # 其他异常转换为存储异常
            raise handle_storage_exception(e, "get_metadata", path)

    def file_exists(self, path: str) -> bool:
        p = self._abs_path(path)
        return p.exists()

    def get_file_url(self, path: str) -> str:
        # Local filesystem path can be served via a static file server
        abs_path = self._abs_path(path).as_posix()
        return f"file://{abs_path}"
