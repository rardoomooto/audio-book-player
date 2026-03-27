"""Storage interface package

This module exposes the storage backends and a factory to obtain the
appropriate storage implementation based on runtime configuration.
"""

from .base import StorageBase
from .webdav import WebDAVStorage
from .local import LocalStorage
from .factory import StorageFactory

__all__ = [
    "StorageBase",
    "WebDAVStorage",
    "LocalStorage",
    "StorageFactory",
]
