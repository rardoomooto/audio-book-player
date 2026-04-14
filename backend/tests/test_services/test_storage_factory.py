"""Storage factory unit tests."""

import pytest
from unittest.mock import patch, MagicMock


class TestStorageFactory:
    @patch("backend.app.services.storage.factory.get_storage_config")
    @patch("backend.app.services.storage.factory.LocalStorage")
    def test_get_storage_returns_local_by_default(self, mock_local, mock_config):
        from backend.app.services.storage.factory import StorageFactory
        mock_config.return_value = {"type": "local", "local": {"mount_path": "/mnt/nas"}}
        mock_local.return_value = MagicMock()

        result = StorageFactory.get_storage()

        mock_local.assert_called_once_with(mount_path="/mnt/nas")

    @patch("backend.app.services.storage.factory.get_storage_config")
    @patch("backend.app.services.storage.factory.LocalStorage")
    def test_get_storage_returns_local_when_type_is_local(self, mock_local, mock_config):
        from backend.app.services.storage.factory import StorageFactory
        mock_config.return_value = {"type": "local", "local": {"mount_path": "/data"}}
        mock_local.return_value = MagicMock()

        result = StorageFactory.get_storage()

        mock_local.assert_called_once()

    @patch("backend.app.services.storage.factory.get_storage_config")
    @patch("backend.app.services.storage.factory.WebDAVStorage")
    def test_get_storage_returns_webdav_when_type_is_webdav(self, mock_webdav, mock_config):
        from backend.app.services.storage.factory import StorageFactory
        mock_config.return_value = {
            "type": "webdav",
            "webdav": {
                "url": "http://nas:5005",
                "username": "admin",
                "password": "secret",
                "timeout": 60,
            },
        }
        mock_webdav.return_value = MagicMock()

        result = StorageFactory.get_storage()

        mock_webdav.assert_called_once()
        call_kwargs = mock_webdav.call_args
        assert call_kwargs[1]["url"] == "http://nas:5005"
        assert call_kwargs[1]["username"] == "admin"

    @patch("backend.app.services.storage.factory.get_storage_config")
    @patch("backend.app.services.storage.factory.LocalStorage")
    def test_get_storage_case_insensitive_type(self, mock_local, mock_config):
        from backend.app.services.storage.factory import StorageFactory
        mock_config.return_value = {"type": "LOCAL", "local": {"mount_path": "/mnt"}}
        mock_local.return_value = MagicMock()

        StorageFactory.get_storage()

        mock_local.assert_called_once()

    @patch("backend.app.services.storage.factory.get_storage_config")
    @patch("backend.app.services.storage.factory.LocalStorage")
    def test_get_storage_none_type_defaults_to_local(self, mock_local, mock_config):
        from backend.app.services.storage.factory import StorageFactory
        mock_config.return_value = {"type": None, "local": {"mount_path": "/mnt"}}
        mock_local.return_value = MagicMock()

        StorageFactory.get_storage()

        mock_local.assert_called_once()

    @patch("backend.app.services.storage.factory.get_storage_config")
    @patch("backend.app.services.storage.factory.LocalStorage")
    def test_get_storage_empty_config(self, mock_local, mock_config):
        from backend.app.services.storage.factory import StorageFactory
        mock_config.return_value = {}
        mock_local.return_value = MagicMock()

        StorageFactory.get_storage()

        mock_local.assert_called_once()

    @patch("backend.app.services.storage.factory.get_storage_config")
    @patch("backend.app.services.storage.factory.WebDAVStorage")
    def test_get_storage_webdav_with_all_options(self, mock_webdav, mock_config):
        from backend.app.services.storage.factory import StorageFactory
        mock_config.return_value = {
            "type": "webdav",
            "webdav": {
                "url": "http://nas:5005",
                "username": "admin",
                "password": "secret",
                "timeout": 60,
                "chunk_size": 32768,
                "verify_ssl": False,
                "cert_path": "/path/cert.pem",
                "key_path": "/path/key.pem",
                "proxy_url": "http://proxy:8080",
                "proxy_username": "proxyuser",
                "proxy_password": "proxypass",
                "recv_speed": 1000,
                "send_speed": 2000,
                "verbose": True,
                "disable_check": True,
            },
        }
        mock_webdav.return_value = MagicMock()

        StorageFactory.get_storage()

        call_kwargs = mock_webdav.call_args[1]
        assert call_kwargs["timeout"] == 60
        assert call_kwargs["chunk_size"] == 32768
        assert call_kwargs["verify_ssl"] is False
        assert call_kwargs["cert_path"] == "/path/cert.pem"
        assert call_kwargs["verbose"] is True
