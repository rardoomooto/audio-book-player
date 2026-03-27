"""内容导入服务。

负责从NAS存储中扫描、提取元数据并导入有声书内容到数据库。
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from ..services.storage.base import StorageBase
from ..services.storage.factory import StorageFactory
from ..utils.storage import is_audio_file, extract_metadata_from_bytes
from ..utils.storage_errors import StorageError, handle_storage_exception
from ..models.content import Content, Folder
from ..core.database import get_db

logger = logging.getLogger(__name__)


@dataclass
class ScanResult:
    """扫描结果。"""
    path: str
    name: str
    size: int
    mtime: float
    is_dir: bool


@dataclass
class AudioMetadata:
    """音频元数据。"""
    path: str
    title: str
    author: Optional[str] = None
    album: Optional[str] = None
    duration: Optional[float] = None
    format: Optional[str] = None
    cover: Optional[bytes] = None
    file_size: int = 0
    mtime: float = 0


@dataclass
class ImportProgress:
    """导入进度。"""
    total_files: int = 0
    processed_files: int = 0
    success_count: int = 0
    error_count: int = 0
    current_file: str = ""
    status: str = "idle"  # idle, scanning, importing, completed, error
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: str = ""


@dataclass
class ImportResult:
    """导入结果。"""
    success: bool
    total_files: int
    imported_files: int
    updated_files: int
    skipped_files: int
    error_files: int
    duration_seconds: float
    errors: List[str]


class IngestionScanner:
    """内容扫描器。"""
    
    def __init__(self, storage: StorageBase):
        self.storage = storage
    
    def scan_directory(self, path: str, recursive: bool = True) -> List[ScanResult]:
        """扫描目录。
        
        Args:
            path: 扫描路径
            recursive: 是否递归扫描
            
        Returns:
            List[ScanResult]: 扫描结果列表
        """
        results = []
        self._scan_recursive(path, results, recursive)
        return results
    
    def _scan_recursive(self, path: str, results: List[ScanResult], recursive: bool):
        """递归扫描目录。"""
        try:
            items = self.storage.list_files(path)
            for item in items:
                if item.is_dir:
                    results.append(ScanResult(
                        path=item.path,
                        name=item.name,
                        size=0,
                        mtime=item.mtime,
                        is_dir=True
                    ))
                    if recursive:
                        self._scan_recursive(item.path, results, recursive)
                else:
                    # 只处理音频文件
                    if is_audio_file(item.path):
                        results.append(ScanResult(
                            path=item.path,
                            name=item.name,
                            size=item.size,
                            mtime=item.mtime,
                            is_dir=False
                        ))
        except StorageError as e:
            logger.error(f"扫描目录失败: {path}, 错误: {e}")
            raise
        except Exception as e:
            logger.error(f"扫描目录异常: {path}, 错误: {e}")
            raise handle_storage_exception(e, "scan_directory", path)
    
    def scan_incremental(self, path: str, last_scan_time: datetime, recursive: bool = True) -> List[ScanResult]:
        """增量扫描目录。
        
        Args:
            path: 扫描路径
            last_scan_time: 上次扫描时间
            recursive: 是否递归扫描
            
        Returns:
            List[ScanResult]: 扫描结果列表（只包含新文件或修改过的文件）
        """
        all_results = self.scan_directory(path, recursive)
        last_scan_timestamp = last_scan_time.timestamp()
        
        # 过滤出新文件或修改过的文件
        incremental_results = [
            result for result in all_results
            if result.mtime > last_scan_timestamp
        ]
        
        return incremental_results


class MetadataExtractor:
    """元数据提取器。"""
    
    def __init__(self, storage: StorageBase):
        self.storage = storage
    
    def extract(self, file_path: str, file_size: int = 0, mtime: float = 0) -> AudioMetadata:
        """提取音频文件元数据。
        
        Args:
            file_path: 文件路径
            file_size: 文件大小
            mtime: 修改时间
            
        Returns:
            AudioMetadata: 音频元数据
        """
        try:
            # 读取文件内容
            data = self.storage.read_file(file_path)
            
            # 提取元数据
            metadata = extract_metadata_from_bytes(data, file_path)
            
            # 使用文件名作为默认标题
            title = metadata.title or Path(file_path).stem
            author = metadata.author
            
            return AudioMetadata(
                path=file_path,
                title=title,
                author=author,
                duration=metadata.duration,
                format=metadata.format,
                cover=metadata.cover,
                file_size=file_size,
                mtime=mtime
            )
        except StorageError as e:
            logger.error(f"提取元数据失败: {file_path}, 错误: {e}")
            # 返回基本元数据
            return AudioMetadata(
                path=file_path,
                title=Path(file_path).stem,
                file_size=file_size,
                mtime=mtime
            )
        except Exception as e:
            logger.error(f"提取元数据异常: {file_path}, 错误: {e}")
            # 返回基本元数据
            return AudioMetadata(
                path=file_path,
                title=Path(file_path).stem,
                file_size=file_size,
                mtime=mtime
            )


class ContentPersister:
    """内容持久化器。"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def persist_content(self, metadata: AudioMetadata) -> Content:
        """持久化内容。
        
        Args:
            metadata: 音频元数据
            
        Returns:
            Content: 内容记录
        """
        # 检查是否已存在
        existing = self.db.query(Content).filter(Content.path == metadata.path).first()
        
        if existing:
            # 更新现有记录
            existing.title = metadata.title
            existing.author = metadata.author
            existing.duration_seconds = int(metadata.duration) if metadata.duration else None
            existing.file_format = metadata.format or "unknown"
            existing.content_metadata = {
                "file_size": metadata.file_size,
                "mtime": metadata.mtime,
                "album": metadata.album,
            }
            existing.updated_at = datetime.utcnow()
            self.db.commit()
            return existing
        else:
            # 创建新记录
            content = Content(
                title=metadata.title,
                author=metadata.author,
                path=metadata.path,
                file_format=metadata.format or "unknown",
                duration_seconds=int(metadata.duration) if metadata.duration else None,
                metadata={
                    "file_size": metadata.file_size,
                    "mtime": metadata.mtime,
                    "album": metadata.album,
                }
            )
            self.db.add(content)
            self.db.commit()
            self.db.refresh(content)
            return content
    
    def persist_folder(self, folder_path: str, folder_name: str, parent_id: Optional[str] = None) -> Folder:
        """持久化文件夹。
        
        Args:
            folder_path: 文件夹路径
            folder_name: 文件夹名称
            parent_id: 父文件夹ID
            
        Returns:
            Folder: 文件夹记录
        """
        # 检查是否已存在
        existing = self.db.query(Folder).filter(Folder.path == folder_path).first()
        
        if existing:
            return existing
        else:
            folder = Folder(
                name=folder_name,
                path=folder_path,
                parent_id=parent_id
            )
            self.db.add(folder)
            self.db.commit()
            self.db.refresh(folder)
            return folder
    
    def cleanup_deleted_files(self, current_files: List[str]) -> int:
        """清理已删除的文件。
        
        Args:
            current_files: 当前文件路径列表
            
        Returns:
            int: 删除的记录数
        """
        # 查找数据库中存在但当前文件列表中不存在的记录
        deleted_count = 0
        all_contents = self.db.query(Content).all()
        
        for content in all_contents:
            if content.path not in current_files:
                self.db.delete(content)
                deleted_count += 1
        
        if deleted_count > 0:
            self.db.commit()
        
        return deleted_count


class IngestionPipeline:
    """内容导入管道。"""
    
    def __init__(self, storage: Optional[StorageBase] = None):
        self.storage = storage or StorageFactory.get_storage()
        self.scanner = IngestionScanner(self.storage)
        self.extractor = MetadataExtractor(self.storage)
        self.progress = ImportProgress()
    
    def run_full_import(self, root_path: str, batch_size: int = 100, max_workers: int = 4) -> ImportResult:
        """运行完整导入。
        
        Args:
            root_path: 根路径
            batch_size: 批次大小
            max_workers: 最大并发数
            
        Returns:
            ImportResult: 导入结果
        """
        start_time = datetime.utcnow()
        self.progress = ImportProgress(
            status="scanning",
            start_time=start_time
        )
        
        try:
            # 1. 扫描目录
            logger.info(f"开始扫描目录: {root_path}")
            scan_results = self.scanner.scan_directory(root_path, recursive=True)
            
            # 过滤出音频文件
            audio_files = [r for r in scan_results if not r.is_dir]
            self.progress.total_files = len(audio_files)
            self.progress.status = "importing"
            
            logger.info(f"扫描完成，找到 {len(audio_files)} 个音频文件")
            
            # 2. 批量处理
            imported_count = 0
            updated_count = 0
            error_count = 0
            errors = []
            current_files = []
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 分批处理
                for i in range(0, len(audio_files), batch_size):
                    batch = audio_files[i:i + batch_size]
                    batch_results = self._process_batch(executor, batch)
                    
                    # 统计结果
                    for result in batch_results:
                        if result["success"]:
                            if result["is_new"]:
                                imported_count += 1
                            else:
                                updated_count += 1
                            current_files.append(result["path"])
                        else:
                            error_count += 1
                            errors.append(result["error"])
                        
                        self.progress.processed_files += 1
                        self.progress.current_file = result["path"]
            
            # 3. 清理已删除的文件
            with get_db() as db:
                persister = ContentPersister(db)
                deleted_count = persister.cleanup_deleted_files(current_files)
            
            # 4. 计算结果
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            self.progress.status = "completed"
            self.progress.end_time = end_time
            self.progress.success_count = imported_count + updated_count
            self.progress.error_count = error_count
            
            return ImportResult(
                success=error_count == 0,
                total_files=len(audio_files),
                imported_files=imported_count,
                updated_files=updated_count,
                skipped_files=0,
                error_files=error_count,
                duration_seconds=duration,
                errors=errors
            )
        
        except Exception as e:
            logger.error(f"导入失败: {e}")
            self.progress.status = "error"
            self.progress.error_message = str(e)
            self.progress.end_time = datetime.utcnow()
            
            return ImportResult(
                success=False,
                total_files=0,
                imported_files=0,
                updated_files=0,
                skipped_files=0,
                error_files=0,
                duration_seconds=0,
                errors=[str(e)]
            )
    
    def run_incremental_import(self, root_path: str, last_scan_time: datetime, batch_size: int = 100, max_workers: int = 4) -> ImportResult:
        """运行增量导入。
        
        Args:
            root_path: 根路径
            last_scan_time: 上次扫描时间
            batch_size: 批次大小
            max_workers: 最大并发数
            
        Returns:
            ImportResult: 导入结果
        """
        start_time = datetime.utcnow()
        self.progress = ImportProgress(
            status="scanning",
            start_time=start_time
        )
        
        try:
            # 1. 增量扫描
            logger.info(f"开始增量扫描: {root_path}, 上次扫描时间: {last_scan_time}")
            scan_results = self.scanner.scan_incremental(root_path, last_scan_time, recursive=True)
            
            # 过滤出音频文件
            audio_files = [r for r in scan_results if not r.is_dir]
            self.progress.total_files = len(audio_files)
            self.progress.status = "importing"
            
            logger.info(f"增量扫描完成，找到 {len(audio_files)} 个新文件或修改过的文件")
            
            # 2. 批量处理
            imported_count = 0
            updated_count = 0
            error_count = 0
            errors = []
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 分批处理
                for i in range(0, len(audio_files), batch_size):
                    batch = audio_files[i:i + batch_size]
                    batch_results = self._process_batch(executor, batch)
                    
                    # 统计结果
                    for result in batch_results:
                        if result["success"]:
                            if result["is_new"]:
                                imported_count += 1
                            else:
                                updated_count += 1
                        else:
                            error_count += 1
                            errors.append(result["error"])
                        
                        self.progress.processed_files += 1
                        self.progress.current_file = result["path"]
            
            # 3. 计算结果
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            self.progress.status = "completed"
            self.progress.end_time = end_time
            self.progress.success_count = imported_count + updated_count
            self.progress.error_count = error_count
            
            return ImportResult(
                success=error_count == 0,
                total_files=len(audio_files),
                imported_files=imported_count,
                updated_files=updated_count,
                skipped_files=0,
                error_files=error_count,
                duration_seconds=duration,
                errors=errors
            )
        
        except Exception as e:
            logger.error(f"增量导入失败: {e}")
            self.progress.status = "error"
            self.progress.error_message = str(e)
            self.progress.end_time = datetime.utcnow()
            
            return ImportResult(
                success=False,
                total_files=0,
                imported_files=0,
                updated_files=0,
                skipped_files=0,
                error_files=0,
                duration_seconds=0,
                errors=[str(e)]
            )
    
    def _process_batch(self, executor: ThreadPoolExecutor, batch: List[ScanResult]) -> List[Dict[str, Any]]:
        """处理批次。
        
        Args:
            executor: 线程池执行器
            batch: 批次文件列表
            
        Returns:
            List[Dict[str, Any]]: 处理结果列表
        """
        results = []
        futures = []
        
        # 提交任务
        for file_info in batch:
            future = executor.submit(self._process_single_file, file_info)
            futures.append((future, file_info))
        
        # 收集结果
        for future, file_info in futures:
            try:
                result = future.result(timeout=60)  # 60秒超时
                results.append(result)
            except Exception as e:
                logger.error(f"处理文件异常: {file_info.path}, 错误: {e}")
                results.append({
                    "path": file_info.path,
                    "success": False,
                    "is_new": False,
                    "error": f"处理异常: {str(e)}"
                })
        
        return results
    
    def _process_single_file(self, file_info: ScanResult) -> Dict[str, Any]:
        """处理单个文件。
        
        Args:
            file_info: 文件信息
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        try:
            # 提取元数据
            metadata = self.extractor.extract(
                file_info.path,
                file_info.size,
                file_info.mtime
            )
            
            # 持久化到数据库
            with get_db() as db:
                persister = ContentPersister(db)
                existing = db.query(Content).filter(Content.path == file_info.path).first()
                is_new = existing is None
                
                content = persister.persist_content(metadata)
                
                return {
                    "path": file_info.path,
                    "success": True,
                    "is_new": is_new,
                    "content_id": content.content_id,
                    "error": ""
                }
        
        except Exception as e:
            logger.error(f"处理文件失败: {file_info.path}, 错误: {e}")
            return {
                "path": file_info.path,
                "success": False,
                "is_new": False,
                "error": f"{file_info.path}: {str(e)}"
            }
    
    def get_progress(self) -> ImportProgress:
        """获取导入进度。
        
        Returns:
            ImportProgress: 导入进度
        """
        return self.progress


# 全局导入管道实例
_ingestion_pipeline: Optional[IngestionPipeline] = None


def get_ingestion_pipeline() -> IngestionPipeline:
    """获取导入管道实例。
    
    Returns:
        IngestionPipeline: 导入管道实例
    """
    global _ingestion_pipeline
    if _ingestion_pipeline is None:
        _ingestion_pipeline = IngestionPipeline()
    return _ingestion_pipeline


def scan_and_import(root_path: str, incremental: bool = False, last_scan_time: Optional[datetime] = None) -> ImportResult:
    """扫描并导入内容。
    
    Args:
        root_path: 根路径
        incremental: 是否增量导入
        last_scan_time: 上次扫描时间（增量导入时需要）
        
    Returns:
        ImportResult: 导入结果
    """
    pipeline = get_ingestion_pipeline()
    
    if incremental and last_scan_time:
        return pipeline.run_incremental_import(root_path, last_scan_time)
    else:
        return pipeline.run_full_import(root_path)