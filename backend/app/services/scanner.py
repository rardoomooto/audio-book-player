"""内容扫描服务。

提供内容扫描和导入功能，使用新的导入管道。
"""

from typing import Dict, Optional
from datetime import datetime

from .ingestion import get_ingestion_pipeline, ImportResult, ImportProgress


class Scanner:
    """内容扫描器。
    
    提供内容扫描和导入功能的包装类，保持向后兼容。
    """
    
    def __init__(self):
        self.progress: int = 0
        self._pipeline = get_ingestion_pipeline()
    
    def scan_nas(self, root_path: str = "/") -> Dict[str, object]:
        """扫描NAS内容。
        
        Args:
            root_path: 扫描根路径，默认为根目录
            
        Returns:
            Dict[str, object]: 扫描结果
        """
        try:
            # 运行完整导入
            result = self._pipeline.run_full_import(root_path)
            
            # 更新进度
            self.progress = 100 if result.success else 0
            
            return {
                "scanned": True,
                "progress": self.progress,
                "total_files": result.total_files,
                "imported_files": result.imported_files,
                "updated_files": result.updated_files,
                "error_files": result.error_files,
                "duration_seconds": result.duration_seconds,
                "errors": result.errors
            }
        except Exception as e:
            self.progress = 0
            return {
                "scanned": False,
                "progress": 0,
                "error": str(e)
            }
    
    def scan_nas_incremental(self, root_path: str, last_scan_time: datetime) -> Dict[str, object]:
        """增量扫描NAS内容。
        
        Args:
            root_path: 扫描根路径
            last_scan_time: 上次扫描时间
            
        Returns:
            Dict[str, object]: 扫描结果
        """
        try:
            # 运行增量导入
            result = self._pipeline.run_incremental_import(root_path, last_scan_time)
            
            # 更新进度
            self.progress = 100 if result.success else 0
            
            return {
                "scanned": True,
                "progress": self.progress,
                "total_files": result.total_files,
                "imported_files": result.imported_files,
                "updated_files": result.updated_files,
                "error_files": result.error_files,
                "duration_seconds": result.duration_seconds,
                "errors": result.errors
            }
        except Exception as e:
            self.progress = 0
            return {
                "scanned": False,
                "progress": 0,
                "error": str(e)
            }
    
    def get_scan_progress(self) -> Dict[str, object]:
        """获取扫描进度。
        
        Returns:
            Dict[str, object]: 进度信息
        """
        progress = self._pipeline.get_progress()
        return {
            "status": progress.status,
            "total_files": progress.total_files,
            "processed_files": progress.processed_files,
            "success_count": progress.success_count,
            "error_count": progress.error_count,
            "current_file": progress.current_file,
            "progress_percent": int(progress.processed_files / progress.total_files * 100) if progress.total_files > 0 else 0
        }
