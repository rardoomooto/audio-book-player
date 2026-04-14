from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from ...schemas.storage import FileInfo, FileMetadata
from ...utils.storage_errors import StorageError


class StorageBase(ABC):
    """Abstract storage backend interface.

    Implementations may be WebDAV, local filesystem, or others later.
    All methods are designed to be side-effect free where possible and
    should raise a compatible exception on errors.
    
    Error Handling:
        所有实现都应该使用 storage_errors 模块中定义的异常类，
        以确保错误处理的一致性。具体来说：
        - StorageConnectionError: 连接相关错误
        - StorageFileNotFoundError: 文件不存在
        - StoragePermissionError: 权限不足
        - StorageTimeoutError: 操作超时
        - StorageError: 其他存储相关错误
    """

    @abstractmethod
    def list_files(self, path: str) -> List[FileInfo]:
        """List files and directories under the given path.

        The result should include both files and directories with
        metadata suitable for navigation in the UI.
        """

    @abstractmethod
    def read_file(self, path: str) -> bytes:
        """Read the raw bytes of a file at the given path."""

    @abstractmethod
    def get_metadata(self, path: str) -> FileMetadata:
        """Extract metadata (title, artist, duration, etc.) from a file."""

    @abstractmethod
    def file_exists(self, path: str) -> bool:
        """Return True if the given path exists in storage."""

    @abstractmethod
    def get_file_url(self, path: str) -> str:
        """Return a URL that can be used to stream or download the file."""
