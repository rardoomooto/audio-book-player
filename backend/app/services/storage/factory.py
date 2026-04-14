from __future__ import annotations

from .base import StorageBase
from .webdav import WebDAVStorage
from .local import LocalStorage
from ...core.config import get_storage_config  # type: ignore


class StorageFactory:
    """Factory to obtain the configured storage backend."""

    @staticmethod
    def get_storage() -> StorageBase:
        cfg = get_storage_config()
        stype = (cfg.get("type") or "local").lower()
        if stype == "webdav":
            web = cfg.get("webdav", {})
            return WebDAVStorage(
                url=web.get("url", ""),
                username=web.get("username"),
                password=web.get("password"),
                timeout=web.get("timeout", 30),
                chunk_size=web.get("chunk_size", 65536),
                verify_ssl=web.get("verify_ssl", True),
                cert_path=web.get("cert_path"),
                key_path=web.get("key_path"),
                proxy_url=web.get("proxy_url"),
                proxy_username=web.get("proxy_username"),
                proxy_password=web.get("proxy_password"),
                recv_speed=web.get("recv_speed"),
                send_speed=web.get("send_speed"),
                verbose=web.get("verbose", False),
                disable_check=web.get("disable_check", False),
                override_methods=web.get("override_methods"),
            )
        else:
            local = cfg.get("local", {})
            return LocalStorage(mount_path=local.get("mount_path"))
