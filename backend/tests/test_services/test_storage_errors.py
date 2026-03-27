"""存储错误处理单元测试。"""

import pytest
from backend.app.utils.storage_errors import (
    StorageError,
    StorageConnectionError,
    StorageFileNotFoundError,
    StoragePermissionError,
    StorageTimeoutError,
    StorageQuotaExceededError,
    StorageFormatError,
    handle_storage_exception,
)


class TestStorageErrors:
    """存储错误类测试。"""

    def test_storage_error_basic(self):
        """测试基础存储错误。"""
        error = StorageError("测试错误", "读取", "/path/to/file")
        assert "测试错误" in str(error)
        assert error.operation == "读取"
        assert error.path == "/path/to/file"

    def test_storage_error_format_message(self):
        """测试错误消息格式化。"""
        error = StorageError("文件损坏", "写入", "/data/audio.mp3")
        message = error._format_message()
        assert "操作: 写入" in message
        assert "路径: /data/audio.mp3" in message
        assert "错误: 文件损坏" in message

    def test_storage_connection_error(self):
        """测试连接错误。"""
        error = StorageConnectionError("无法连接到服务器", "http://nas.local", 3)
        assert "无法连接到服务器" in str(error)
        assert error.url == "http://nas.local"
        assert error.retry_count == 3

    def test_storage_file_not_found_error(self):
        """测试文件不存在错误。"""
        error = StorageFileNotFoundError("/path/to/missing.mp3")
        assert "文件不存在" in str(error)
        assert error.path == "/path/to/missing.mp3"

    def test_storage_permission_error(self):
        """测试权限错误。"""
        error = StoragePermissionError("/protected/file.mp3", "读取")
        assert "权限不足" in str(error)
        assert error.path == "/protected/file.mp3"
        assert error.operation == "读取"

    def test_storage_timeout_error(self):
        """测试超时错误。"""
        error = StorageTimeoutError("下载", "/large/file.mp3", 30.0)
        assert "操作超时" in str(error)
        assert error.timeout == 30.0
        assert error.path == "/large/file.mp3"

    def test_storage_quota_exceeded_error(self):
        """测试配额超出错误。"""
        error = StorageQuotaExceededError("/upload/file.mp3")
        assert "存储配额已满" in str(error)

    def test_storage_format_error(self):
        """测试格式错误。"""
        error = StorageFormatError("/invalid/file.xyz", "mp3")
        assert "文件格式不支持" in str(error)
        assert "期望: mp3" in str(error)


class TestHandleStorageException:
    """异常转换测试。"""

    def test_handle_connection_error(self):
        """测试连接异常转换。"""
        original = Exception("Connection refused")
        result = handle_storage_exception(original, "read_file", "/test")
        assert isinstance(result, StorageConnectionError)

    def test_handle_not_found_error(self):
        """测试文件不存在异常转换。"""
        original = Exception("File not found: 404")
        result = handle_storage_exception(original, "read_file", "/test")
        assert isinstance(result, StorageFileNotFoundError)

    def test_handle_permission_error(self):
        """测试权限异常转换。"""
        original = Exception("403 Forbidden")
        result = handle_storage_exception(original, "read_file", "/test")
        assert isinstance(result, StoragePermissionError)

    def test_handle_timeout_error(self):
        """测试超时异常转换。"""
        original = Exception("Operation timeout")
        result = handle_storage_exception(original, "download", "/test")
        assert isinstance(result, StorageTimeoutError)

    def test_handle_generic_error(self):
        """测试通用异常转换。"""
        original = Exception("Unknown error")
        result = handle_storage_exception(original, "read_file", "/test")
        assert isinstance(result, StorageError)
        assert not isinstance(result, StorageConnectionError)

    def test_handle_storage_error_passthrough(self):
        """测试存储异常直接传递。"""
        original = StorageFileNotFoundError("/test")
        result = handle_storage_exception(original, "read_file", "/test")
        assert result is original