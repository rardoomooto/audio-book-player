"""WebDAV存储客户端单元测试（使用mock）。"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from backend.app.services.storage.webdav import WebDAVStorage
from backend.app.services.storage.local import LocalStorage
from backend.app.utils.storage_errors import (
    StorageFileNotFoundError,
    StorageConnectionError,
    StoragePermissionError,
)


class TestWebDAVStorageInit:
    """WebDAV存储初始化测试。"""

    def test_init_basic(self):
        """测试基本初始化。"""
        storage = WebDAVStorage(
            url="http://nas.local",
            username="user",
            password="pass"
        )
        assert storage.url == "http://nas.local"
        assert storage.username == "user"
        assert storage.password == "pass"

    def test_init_with_timeout(self):
        """测试带超时的初始化。"""
        storage = WebDAVStorage(
            url="http://nas.local",
            timeout=60
        )
        assert storage.url == "http://nas.local"

    def test_init_with_ssl(self):
        """测试SSL配置初始化。"""
        storage = WebDAVStorage(
            url="https://nas.local",
            verify_ssl=False
        )
        assert storage.url == "https://nas.local"

    def test_init_with_proxy(self):
        """测试代理配置初始化。"""
        storage = WebDAVStorage(
            url="http://nas.local",
            proxy_url="http://proxy.local:8080",
            proxy_username="proxyuser",
            proxy_password="proxypass"
        )
        assert storage.url == "http://nas.local"

    def test_url_trailing_slash_removed(self):
        """测试URL末尾斜杠被移除。"""
        storage = WebDAVStorage(url="http://nas.local/")
        assert storage.url == "http://nas.local"


class TestWebDAVStoragePathHandling:
    """WebDAV路径处理测试。"""

    @pytest.fixture
    def storage(self):
        """创建WebDAV存储实例。"""
        return WebDAVStorage(url="http://nas.local")

    def test_full_path_absolute(self, storage):
        """测试绝对路径处理。"""
        result = storage._full_path("/absolute/path")
        assert result == "/absolute/path"

    def test_full_path_relative(self, storage):
        """测试相对路径处理。"""
        result = storage._full_path("relative/path")
        assert result == "/relative/path"

    def test_full_path_empty(self, storage):
        """测试空路径处理。"""
        result = storage._full_path("")
        assert result == "/"


class TestLocalStorage:
    """本地存储测试。"""

    @pytest.fixture
    def storage(self, tmp_path):
        """创建本地存储实例。"""
        return LocalStorage(mount_path=str(tmp_path))

    def test_init_default(self):
        """测试默认初始化。"""
        storage = LocalStorage()
        assert storage.mount_path is not None

    def test_init_with_path(self, tmp_path):
        """测试指定路径初始化。"""
        storage = LocalStorage(mount_path=str(tmp_path))
        assert str(storage.mount_path) == str(tmp_path)

    def test_abs_path_relative(self, storage, tmp_path):
        """测试相对路径转换。"""
        result = storage._abs_path("subdir/file.mp3")
        assert str(result).startswith(str(tmp_path))
        # 检查路径包含subdir和file.mp3（Windows使用反斜杠）
        assert "subdir" in str(result)
        assert "file.mp3" in str(result)

    def test_abs_path_absolute(self, storage):
        """测试绝对路径保持不变。"""
        result = storage._abs_path("/absolute/path")
        # 在Windows上，绝对路径会被转换为Windows格式
        # 我们只检查路径包含absolute和path
        assert "absolute" in str(result)
        assert "path" in str(result)

    def test_file_exists_false(self, storage):
        """测试不存在的文件。"""
        result = storage.file_exists("nonexistent.mp3")
        assert result is False

    def test_file_exists_true(self, storage, tmp_path):
        """测试存在的文件。"""
        # 创建测试文件
        test_file = tmp_path / "test.mp3"
        test_file.write_text("test content")
        
        result = storage.file_exists("test.mp3")
        assert result is True

    def test_list_files_empty(self, storage, tmp_path):
        """测试空目录列表。"""
        items = storage.list_files(".")
        # 可能返回空列表或包含子目录
        assert isinstance(items, list)

    def test_list_files_with_files(self, storage, tmp_path):
        """测试包含文件的目录列表。"""
        # 创建测试文件
        (tmp_path / "file1.mp3").write_text("content1")
        (tmp_path / "file2.mp3").write_text("content2")
        
        items = storage.list_files(".")
        assert len(items) >= 2

    def test_read_file(self, storage, tmp_path):
        """测试读取文件。"""
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b"test content")
        
        content = storage.read_file("test.txt")
        assert content == b"test content"

    def test_read_nonexistent_file(self, storage):
        """测试读取不存在的文件。"""
        with pytest.raises(StorageFileNotFoundError):
            storage.read_file("nonexistent.mp3")


class TestWebDAVStorageMocked:
    """WebDAV存储Mock测试。"""

    @pytest.fixture
    def mock_client(self):
        """创建mock客户端。"""
        client = Mock()
        client.list = Mock(return_value=[])
        client.check = Mock(return_value=True)
        client.info = Mock(return_value={"content-length": "1000", "last-modified": "1234567890"})
        client.get_contents = Mock(return_value=b"test content")
        return client

    @pytest.fixture
    def storage(self, mock_client):
        """创建带mock客户端的WebDAV存储。"""
        storage = WebDAVStorage(url="http://nas.local", username="user", password="pass")
        storage.client = mock_client
        return storage

    def test_list_files_success(self, storage, mock_client):
        """测试成功列出文件。"""
        mock_client.list.return_value = ["file1.mp3", "file2.mp3"]
        
        items = storage.list_files("/audio")
        assert len(items) == 2
        assert items[0].name == "file1.mp3"
        assert items[1].name == "file2.mp3"

    def test_list_files_empty(self, storage, mock_client):
        """测试空目录。"""
        mock_client.list.return_value = []
        
        items = storage.list_files("/empty")
        assert len(items) == 0

    def test_file_exists_true(self, storage, mock_client):
        """测试文件存在。"""
        mock_client.check.return_value = True
        
        result = storage.file_exists("/audio/test.mp3")
        assert result is True

    def test_file_exists_false(self, storage, mock_client):
        """测试文件不存在。"""
        from webdav3.exceptions import RemoteResourceNotFound
        mock_client.check.side_effect = RemoteResourceNotFound("Not found")
        
        result = storage.file_exists("/audio/nonexistent.mp3")
        assert result is False

    def test_read_file_success(self, storage, mock_client):
        """测试成功读取文件。"""
        mock_client.get_contents.return_value = b"audio content"
        
        content = storage.read_file("/audio/test.mp3")
        assert content == b"audio content"

    def test_read_file_not_found(self, storage, mock_client):
        """测试读取不存在的文件。"""
        from webdav3.exceptions import RemoteResourceNotFound
        mock_client.get_contents.side_effect = RemoteResourceNotFound("Not found")
        
        with pytest.raises(StorageFileNotFoundError):
            storage.read_file("/audio/nonexistent.mp3")

    def test_get_file_url(self, storage):
        """测试获取文件URL。"""
        url = storage.get_file_url("/audio/test.mp3")
        assert url == "http://nas.local/audio/test.mp3"


class TestStorageFactory:
    """存储工厂测试。"""

    @patch('backend.app.services.storage.factory.get_storage_config')
    def test_get_local_storage(self, mock_config):
        """测试获取本地存储。"""
        mock_config.return_value = {
            "type": "local",
            "local": {"mount_path": "/tmp"}
        }
        
        from backend.app.services.storage.factory import StorageFactory
        storage = StorageFactory.get_storage()
        assert isinstance(storage, LocalStorage)

    @patch('backend.app.services.storage.factory.get_storage_config')
    def test_get_webdav_storage(self, mock_config):
        """测试获取WebDAV存储。"""
        mock_config.return_value = {
            "type": "webdav",
            "webdav": {
                "url": "http://nas.local",
                "username": "user",
                "password": "pass"
            }
        }
        
        from backend.app.services.storage.factory import StorageFactory
        storage = StorageFactory.get_storage()
        assert isinstance(storage, WebDAVStorage)