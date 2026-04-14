"""Application configuration using Pydantic BaseSettings."""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AudioBook Player"
    description: str = "FastAPI skeleton for home audiobook player"
    version: str = "0.1.0"

    environment: str = "development"

    # Database URL for SQLAlchemy (async)
    database_url: str = "sqlite+aiosqlite:///./sqlite.db"

    # Simple JWT configuration
    jwt_secret_key: str = "CHANGE_ME"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15

    # CORS / origins (for dev, allow all)
    allowed_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
import os
from typing import Optional

# Simple, environment-driven storage configuration

_STORAGE_TYPE_ENV = os.getenv("STORAGE_TYPE", "local").lower()
WEBDAV_URL_ENV = os.getenv("WEBDAV_URL")
WEBDAV_USERNAME_ENV = os.getenv("WEBDAV_USERNAME")
WEBDAV_PASSWORD_ENV = os.getenv("WEBDAV_PASSWORD")
LOCAL_MOUNT_PATH_ENV = os.getenv("LOCAL_MOUNT_PATH")

# WebDAV高级配置
WEBDAV_TIMEOUT_ENV = int(os.getenv("WEBDAV_TIMEOUT", "30"))
WEBDAV_CHUNK_SIZE_ENV = int(os.getenv("WEBDAV_CHUNK_SIZE", "65536"))
WEBDAV_VERIFY_SSL_ENV = os.getenv("WEBDAV_VERIFY_SSL", "true").lower() == "true"
WEBDAV_CERT_PATH_ENV = os.getenv("WEBDAV_CERT_PATH")
WEBDAV_KEY_PATH_ENV = os.getenv("WEBDAV_KEY_PATH")
WEBDAV_PROXY_URL_ENV = os.getenv("WEBDAV_PROXY_URL")
WEBDAV_PROXY_USERNAME_ENV = os.getenv("WEBDAV_PROXY_USERNAME")
WEBDAV_PROXY_PASSWORD_ENV = os.getenv("WEBDAV_PROXY_PASSWORD")
WEBDAV_RECV_SPEED_ENV: Optional[int] = int(os.getenv("WEBDAV_RECV_SPEED")) if os.getenv("WEBDAV_RECV_SPEED") else None
WEBDAV_SEND_SPEED_ENV: Optional[int] = int(os.getenv("WEBDAV_SEND_SPEED")) if os.getenv("WEBDAV_SEND_SPEED") else None
WEBDAV_VERBOSE_ENV = os.getenv("WEBDAV_VERBOSE", "false").lower() == "true"
WEBDAV_DISABLE_CHECK_ENV = os.getenv("WEBDAV_DISABLE_CHECK", "false").lower() == "true"


def get_storage_config() -> dict:
    """Return storage configuration as a dict understood by the storage factory.

    This is a lightweight adapter over environment variables to keep the
    code decoupled from any particular configuration framework.
    """
    config = {
        "type": _STORAGE_TYPE_ENV,
        "webdav": {
            "url": WEBDAV_URL_ENV,
            "username": WEBDAV_USERNAME_ENV,
            "password": WEBDAV_PASSWORD_ENV,
            "timeout": WEBDAV_TIMEOUT_ENV,
            "chunk_size": WEBDAV_CHUNK_SIZE_ENV,
            "verify_ssl": WEBDAV_VERIFY_SSL_ENV,
            "cert_path": WEBDAV_CERT_PATH_ENV,
            "key_path": WEBDAV_KEY_PATH_ENV,
            "proxy_url": WEBDAV_PROXY_URL_ENV,
            "proxy_username": WEBDAV_PROXY_USERNAME_ENV,
            "proxy_password": WEBDAV_PROXY_PASSWORD_ENV,
            "recv_speed": WEBDAV_RECV_SPEED_ENV,
            "send_speed": WEBDAV_SEND_SPEED_ENV,
            "verbose": WEBDAV_VERBOSE_ENV,
            "disable_check": WEBDAV_DISABLE_CHECK_ENV,
        },
        "local": {
            "mount_path": LOCAL_MOUNT_PATH_ENV,
        },
    }
    return config
