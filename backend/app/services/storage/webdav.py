from __future__ import annotations

import io
import os
from typing import List, Optional, Dict, Any

from webdav3.client import Client  # type: ignore
from webdav3.exceptions import (  # type: ignore
    WebDavException,
    RemoteResourceNotFound,
    NotFound,
    ConnectionException,
    NoConnection,
    ResponseErrorCode,
)

from .base import StorageBase
from ...schemas.storage import FileInfo, FileMetadata
from ...utils.storage import is_audio_file, extract_metadata_from_bytes
from ...utils.storage_errors import (
    StorageConnectionError,
    StorageFileNotFoundError,
    StoragePermissionError,
    StorageTimeoutError,
    handle_storage_exception,
)


class WebDAVStorage(StorageBase):
    """WebDAV-backed storage implementation.
    
    支持完整的WebDAV配置，包括超时、代理、证书、带宽限制等。
    基于webdavclient3库，提供生产环境级别的可靠性。
    """

    def __init__(
        self,
        url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        verify_ssl: bool = True,
        cert_path: Optional[str] = None,
        key_path: Optional[str] = None,
        proxy_url: Optional[str] = None,
        proxy_username: Optional[str] = None,
        proxy_password: Optional[str] = None,
        recv_speed: Optional[int] = None,
        send_speed: Optional[int] = None,
        verbose: bool = False,
        disable_check: bool = False,
        override_methods: Optional[Dict[str, str]] = None,
    ):
        """初始化WebDAV存储。
        
        Args:
            url: WebDAV服务器地址
            username: 用户名
            password: 密码
            timeout: 请求超时时间（秒），默认30
            chunk_size: 分块大小（字节），默认65536
            verify_ssl: 是否验证SSL证书，默认True
            cert_path: 客户端证书路径
            key_path: 客户端密钥路径
            proxy_url: 代理服务器地址
            proxy_username: 代理用户名
            proxy_password: 代理密码
            recv_speed: 接收速度限制（字节/秒）
            send_speed: 发送速度限制（字节/秒）
            verbose: 是否启用详细日志
            disable_check: 是否禁用资源检查
            override_methods: 覆盖HTTP方法映射
        """
        self.url = url.rstrip("/")
        self.username = username or ""
        self.password = password or ""
        
        # 构建配置字典
        options: Dict[str, Any] = {
            "webdav_hostname": self.url,
            "webdav_login": self.username,
            "webdav_password": self.password,
            "webdav_timeout": timeout,
            "chunk_size": chunk_size,
            "verbose": verbose,
            "disable_check": disable_check,
        }
        
        # SSL证书配置
        if not verify_ssl:
            options["verify"] = False
        if cert_path:
            options["cert_path"] = cert_path
        if key_path:
            options["key_path"] = key_path
        
        # 代理配置
        if proxy_url:
            options["proxy_hostname"] = proxy_url
            if proxy_username:
                options["proxy_login"] = proxy_username
            if proxy_password:
                options["proxy_password"] = proxy_password
        
        # 带宽限制
        if recv_speed:
            options["recv_speed"] = recv_speed
        if send_speed:
            options["send_speed"] = send_speed
        
        # 方法覆盖
        if override_methods:
            options["webdav_override_methods"] = override_methods
        
        # 创建客户端
        self.client = Client(options)
        
        # 如果不验证SSL证书，设置客户端属性
        if not verify_ssl:
            self.client.verify = False

    def _full_path(self, path: str) -> str:
        if path.startswith("/"):
            return path
        return "/" + path

    def list_files(self, path: str) -> List[FileInfo]:
        path = self._full_path(path)
        items: List[FileInfo] = []
        try:
            entries = self.client.list(path)
        except RemoteResourceNotFound:
            # 路径不存在，返回空列表
            return items
        except NotFound:
            # 路径不存在，返回空列表
            return items
        except ConnectionException as e:
            raise StorageConnectionError(str(e), self.url)
        except NoConnection as e:
            raise StorageConnectionError(str(e), self.url)
        except WebDavException as e:
            # 其他WebDAV错误，尝试作为文件处理
            if self.file_exists(path):
                md = self.get_metadata(path)
                items.append(
                    FileInfo(
                        name=os.path.basename(path),
                        path=path,
                        size=md.duration or 0,
                        mtime=0,
                        is_dir=False,
                    )
                )
            return items
        except Exception as e:
            # 其他异常，尝试作为文件处理
            if self.file_exists(path):
                md = self.get_metadata(path)
                items.append(
                    FileInfo(
                        name=os.path.basename(path),
                        path=path,
                        size=md.duration or 0,
                        mtime=0,
                        is_dir=False,
                    )
                )
            return items

        for name in entries:
            item_path = path.rstrip("/") + "/" + name
            try:
                info = self.client.info(item_path)
                size = int(info.get("content-length") or info.get("size") or 0)
                mtime = info.get("last-modified") or 0
            except Exception as e:
                # 记录警告但继续处理
                size = 0
                mtime = 0
            # Heuristic: directories might be indicated by trailing '/'
            is_dir = False
            try:
                if isinstance(entries, list) and name.endswith("/"):
                    is_dir = True
            except Exception:
                pass
            items.append(
                FileInfo(
                    name=name.rstrip("/"),
                    path=item_path,
                    size=size,
                    mtime=float(mtime) if mtime else 0.0,
                    is_dir=is_dir,
                )
            )
        return items

    def read_file(self, path: str) -> bytes:
        path = self._full_path(path)
        try:
            # webdav3 provides get_contents
            data = self.client.get_contents(path)
            if isinstance(data, bytes):
                return data
            if isinstance(data, bytearray):
                return bytes(data)
            # Fallback: write to temp and read back
            with io.BytesIO() as bio:
                bio.write(data if isinstance(data, (bytes, bytearray)) else b"")
                return bio.getvalue()
        except RemoteResourceNotFound:
            raise StorageFileNotFoundError(path)
        except NotFound:
            raise StorageFileNotFoundError(path)
        except ConnectionException as e:
            raise StorageConnectionError(str(e), self.url)
        except NoConnection as e:
            raise StorageConnectionError(str(e), self.url)
        except ResponseErrorCode as e:
            # 检查HTTP状态码
            error_msg = str(e).lower()
            if "404" in error_msg:
                raise StorageFileNotFoundError(path)
            elif "401" in error_msg or "403" in error_msg:
                raise StoragePermissionError(path, "读取")
            else:
                raise handle_storage_exception(e, "read_file", path)
        except WebDavException as e:
            raise handle_storage_exception(e, "read_file", path)
        except Exception as e:
            raise handle_storage_exception(e, "read_file", path)

    def get_metadata(self, path: str) -> FileMetadata:
        data = self.read_file(path)
        meta = extract_metadata_from_bytes(data, path)
        return meta

    def file_exists(self, path: str) -> bool:
        path = self._full_path(path)
        try:
            return bool(self.client.check(path))
        except RemoteResourceNotFound:
            return False
        except NotFound:
            return False
        except ConnectionException as e:
            raise StorageConnectionError(str(e), self.url)
        except NoConnection as e:
            raise StorageConnectionError(str(e), self.url)
        except WebDavException:
            # 其他WebDAV错误，尝试通过info检查
            try:
                self.client.info(path)
                return True
            except Exception:
                return False
        except Exception:
            # 其他异常，尝试通过info检查
            try:
                self.client.info(path)
                return True
            except Exception:
                return False

    def get_file_url(self, path: str) -> str:
        # WebDAV URL for direct access
        # 注意：这需要WebDAV服务器支持直接访问，或者需要认证信息
        return f"{self.url}{self._full_path(path)}"
    
    def download_file(self, remote_path: str, local_path: str) -> bool:
        """下载文件到本地。
        
        Args:
            remote_path: 远程文件路径
            local_path: 本地文件路径
            
        Returns:
            bool: 下载是否成功
            
        Raises:
            StorageFileNotFoundError: 远程文件不存在
            StorageConnectionError: 连接错误
            StoragePermissionError: 权限错误
        """
        remote_path = self._full_path(remote_path)
        try:
            # 使用webdav3的download方法
            self.client.download(remote_path, local_path)
            return True
        except RemoteResourceNotFound:
            raise StorageFileNotFoundError(remote_path)
        except NotFound:
            raise StorageFileNotFoundError(remote_path)
        except ConnectionException as e:
            raise StorageConnectionError(str(e), self.url)
        except NoConnection as e:
            raise StorageConnectionError(str(e), self.url)
        except ResponseErrorCode as e:
            error_msg = str(e).lower()
            if "404" in error_msg:
                raise StorageFileNotFoundError(remote_path)
            elif "401" in error_msg or "403" in error_msg:
                raise StoragePermissionError(remote_path, "下载")
            else:
                raise handle_storage_exception(e, "download_file", remote_path)
        except WebDavException as e:
            raise handle_storage_exception(e, "download_file", remote_path)
        except Exception as e:
            raise handle_storage_exception(e, "download_file", remote_path)
    
    def download_file_to_stream(self, remote_path: str, file_stream) -> bool:
        """下载文件到文件流。
        
        Args:
            remote_path: 远程文件路径
            file_stream: 文件流对象（可写）
            
        Returns:
            bool: 下载是否成功
            
        Raises:
            StorageFileNotFoundError: 远程文件不存在
            StorageConnectionError: 连接错误
            StoragePermissionError: 权限错误
        """
        remote_path = self._full_path(remote_path)
        try:
            # 使用webdav3的download方法，传入文件流
            self.client.download(remote_path, file_stream)
            return True
        except RemoteResourceNotFound:
            raise StorageFileNotFoundError(remote_path)
        except NotFound:
            raise StorageFileNotFoundError(remote_path)
        except ConnectionException as e:
            raise StorageConnectionError(str(e), self.url)
        except NoConnection as e:
            raise StorageConnectionError(str(e), self.url)
        except ResponseErrorCode as e:
            error_msg = str(e).lower()
            if "404" in error_msg:
                raise StorageFileNotFoundError(remote_path)
            elif "401" in error_msg or "403" in error_msg:
                raise StoragePermissionError(remote_path, "下载")
            else:
                raise handle_storage_exception(e, "download_file_to_stream", remote_path)
        except WebDavException as e:
            raise handle_storage_exception(e, "download_file_to_stream", remote_path)
        except Exception as e:
            raise handle_storage_exception(e, "download_file_to_stream", remote_path)
