"""Config module unit tests."""

import os
import importlib
import pytest


class TestSettingsDefaults:
    def test_default_app_name(self):
        from backend.app.core.config import Settings
        s = Settings()
        assert s.app_name == "AudioBook Player"

    def test_default_version(self):
        from backend.app.core.config import Settings
        s = Settings()
        assert s.version == "0.1.0"

    def test_default_database_url(self):
        from backend.app.core.config import Settings
        s = Settings()
        assert "sqlite" in s.database_url

    def test_default_jwt_secret(self):
        from backend.app.core.config import Settings
        s = Settings()
        assert s.jwt_secret_key == "CHANGE_ME"

    def test_default_jwt_algorithm(self):
        from backend.app.core.config import Settings
        s = Settings()
        assert s.jwt_algorithm == "HS256"

    def test_default_jwt_expire_minutes(self):
        from backend.app.core.config import Settings
        s = Settings()
        assert s.jwt_access_token_expire_minutes == 15

    def test_default_allowed_origins(self):
        from backend.app.core.config import Settings
        s = Settings()
        assert s.allowed_origins == ["*"]

    def test_default_environment(self):
        from backend.app.core.config import Settings
        s = Settings()
        assert s.environment == "development"


class TestSettingsEnvOverride:
    def test_env_override_app_name(self, monkeypatch):
        monkeypatch.setenv("APP_NAME", "TestApp")
        from backend.app.core.config import Settings
        s = Settings()
        assert s.app_name == "TestApp"

    def test_env_override_database_url(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "postgresql://test/db")
        from backend.app.core.config import Settings
        s = Settings()
        assert s.database_url == "postgresql://test/db"

    def test_env_override_jwt_secret(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET_KEY", "super-secret-key")
        from backend.app.core.config import Settings
        s = Settings()
        assert s.jwt_secret_key == "super-secret-key"


class TestGetSettings:
    def test_get_settings_returns_settings_instance(self):
        from backend.app.core.config import get_settings, Settings
        result = get_settings()
        assert isinstance(result, Settings)


class TestStorageConfig:
    def test_get_storage_config_returns_dict(self):
        from backend.app.core.config import get_storage_config
        config = get_storage_config()
        assert isinstance(config, dict)
        assert "type" in config
        assert "webdav" in config
        assert "local" in config

    def test_default_storage_type(self):
        from backend.app.core.config import get_storage_config
        config = get_storage_config()
        assert config["type"] == "local"

    def test_webdav_config_structure(self):
        from backend.app.core.config import get_storage_config
        config = get_storage_config()
        webdav = config["webdav"]
        assert "url" in webdav
        assert "username" in webdav
        assert "password" in webdav
        assert "timeout" in webdav
        assert "chunk_size" in webdav
        assert "verify_ssl" in webdav

    def test_local_config_structure(self):
        from backend.app.core.config import get_storage_config
        config = get_storage_config()
        local = config["local"]
        assert "mount_path" in local

    def test_webdav_timeout_default(self):
        from backend.app.core.config import get_storage_config
        config = get_storage_config()
        assert config["webdav"]["timeout"] == 30

    def test_webdav_chunk_size_default(self):
        from backend.app.core.config import get_storage_config
        config = get_storage_config()
        assert config["webdav"]["chunk_size"] == 65536

    def test_webdav_verify_ssl_default(self):
        from backend.app.core.config import get_storage_config
        config = get_storage_config()
        assert config["webdav"]["verify_ssl"] is True

    def test_storage_type_env_override(self, monkeypatch):
        monkeypatch.setenv("STORAGE_TYPE", "webdav")
        import backend.app.core.config as config_module
        importlib.reload(config_module)
        config = config_module.get_storage_config()
        assert config["type"] == "webdav"

    def test_local_mount_path_env(self, monkeypatch):
        monkeypatch.setenv("LOCAL_MOUNT_PATH", "/mnt/nas")
        import backend.app.core.config as config_module
        importlib.reload(config_module)
        config = config_module.get_storage_config()
        assert config["local"]["mount_path"] == "/mnt/nas"

    def test_webdav_url_env(self, monkeypatch):
        monkeypatch.setenv("WEBDAV_URL", "http://nas:5005")
        import backend.app.core.config as config_module
        importlib.reload(config_module)
        config = config_module.get_storage_config()
        assert config["webdav"]["url"] == "http://nas:5005"

    def test_webdav_timeout_env_override(self, monkeypatch):
        monkeypatch.setenv("WEBDAV_TIMEOUT", "60")
        import backend.app.core.config as config_module
        importlib.reload(config_module)
        config = config_module.get_storage_config()
        assert config["webdav"]["timeout"] == 60

    def test_webdav_verify_ssl_env_false(self, monkeypatch):
        monkeypatch.setenv("WEBDAV_VERIFY_SSL", "false")
        import backend.app.core.config as config_module
        importlib.reload(config_module)
        config = config_module.get_storage_config()
        assert config["webdav"]["verify_ssl"] is False

    def test_webdav_verbose_env(self, monkeypatch):
        monkeypatch.setenv("WEBDAV_VERBOSE", "true")
        import backend.app.core.config as config_module
        importlib.reload(config_module)
        config = config_module.get_storage_config()
        assert config["webdav"]["verbose"] is True

    def test_webdav_disable_check_env(self, monkeypatch):
        monkeypatch.setenv("WEBDAV_DISABLE_CHECK", "true")
        import backend.app.core.config as config_module
        importlib.reload(config_module)
        config = config_module.get_storage_config()
        assert config["webdav"]["disable_check"] is True

    def test_webdav_recv_speed_none_by_default(self):
        from backend.app.core.config import get_storage_config
        config = get_storage_config()
        assert config["webdav"]["recv_speed"] is None

    def test_webdav_send_speed_none_by_default(self):
        from backend.app.core.config import get_storage_config
        config = get_storage_config()
        assert config["webdav"]["send_speed"] is None

    def test_webdav_cert_path_none_by_default(self):
        from backend.app.core.config import get_storage_config
        config = get_storage_config()
        assert config["webdav"]["cert_path"] is None

    def test_webdav_proxy_none_by_default(self):
        from backend.app.core.config import get_storage_config
        config = get_storage_config()
        assert config["webdav"]["proxy_url"] is None
        assert config["webdav"]["proxy_username"] is None
        assert config["webdav"]["proxy_password"] is None
