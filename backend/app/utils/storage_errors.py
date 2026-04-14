"""统一存储错误处理模块。

定义存储层相关的异常类，提供一致的错误处理机制。
"""

from typing import Optional


class StorageError(Exception):
    """存储操作基础异常类。"""
    
    def __init__(self, message: str, operation: str = "", path: str = ""):
        self.message = message
        self.operation = operation
        self.path = path
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        parts = []
        if self.operation:
            parts.append(f"操作: {self.operation}")
        if self.path:
            parts.append(f"路径: {self.path}")
        parts.append(f"错误: {self.message}")
        return " | ".join(parts)


class StorageConnectionError(StorageError):
    """存储连接错误。"""
    
    def __init__(self, message: str, url: str = "", retry_count: int = 0):
        self.url = url
        self.retry_count = retry_count
        super().__init__(message, "连接")


class StorageFileNotFoundError(StorageError):
    """文件不存在错误。"""
    
    def __init__(self, path: str):
        super().__init__("文件不存在", "访问", path)


class StoragePermissionError(StorageError):
    """存储权限错误。"""
    
    def __init__(self, path: str, operation: str = "访问"):
        super().__init__("权限不足", operation, path)


class StorageTimeoutError(StorageError):
    """存储操作超时错误。"""
    
    def __init__(self, operation: str, path: str = "", timeout: float = 0):
        self.timeout = timeout
        message = f"操作超时 ({timeout}秒)"
        super().__init__(message, operation, path)


class StorageQuotaExceededError(StorageError):
    """存储配额超出错误。"""
    
    def __init__(self, path: str = ""):
        super().__init__("存储配额已满", "写入", path)


class StorageFormatError(StorageError):
    """存储格式错误。"""
    
    def __init__(self, path: str, expected_format: str = ""):
        message = "文件格式不支持"
        if expected_format:
            message += f"，期望: {expected_format}"
        super().__init__(message, "读取", path)


def handle_storage_exception(e: Exception, operation: str, path: str = "") -> StorageError:
    """将通用异常转换为存储异常。    
    Args:
        e: 原始异常
        operation: 操作类型
        path: 文件路径        
    Returns:
        StorageError: 转换后的存储异常
    """
    if isinstance(e, StorageError):
        return e
    
    error_msg = str(e).lower()
    
    # 超时错误（优先检查）
    if "timeout" in error_msg:
        return StorageTimeoutError(operation, path)
    
    # 连接相关错误
    if any(keyword in error_msg for keyword in ["connection", "connect", "network"]):
        return StorageConnectionError(str(e))
    
    # 文件不存在
    if any(keyword in error_msg for keyword in ["not found", "no such file", "404"]):
        return StorageFileNotFoundError(path)
    
    # 权限错误
    if any(keyword in error_msg for keyword in ["permission", "forbidden", "401", "403"]):
        return StoragePermissionError(path, operation)
    
    # 默认返回通用存储错误
    return StorageError(str(e), operation, path)