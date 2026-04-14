"""内容导入管道单元测试。"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from backend.app.services.ingestion import (
    IngestionScanner,
    MetadataExtractor,
    ContentPersister,
    IngestionPipeline,
    ScanResult,
    AudioMetadata,
    ImportProgress,
    ImportResult,
)


class TestScanResult:
    """扫描结果测试。"""

    def test_scan_result_creation(self):
        """测试扫描结果创建。"""
        result = ScanResult(
            path="/audio/test.mp3",
            name="test.mp3",
            size=1024,
            mtime=1234567890.0,
            is_dir=False
        )
        assert result.path == "/audio/test.mp3"
        assert result.name == "test.mp3"
        assert result.size == 1024
        assert result.is_dir is False


class TestAudioMetadata:
    """音频元数据测试。"""

    def test_audio_metadata_creation(self):
        """测试音频元数据创建。"""
        metadata = AudioMetadata(
            path="/audio/test.mp3",
            title="Test Track",
            author="Test Artist",
            duration=180.5,
            format="mp3"
        )
        assert metadata.title == "Test Track"
        assert metadata.author == "Test Artist"
        assert metadata.duration == 180.5

    def test_audio_metadata_defaults(self):
        """测试音频元数据默认值。"""
        metadata = AudioMetadata(
            path="/audio/test.mp3",
            title="Test Track"
        )
        assert metadata.author is None
        assert metadata.album is None
        assert metadata.duration is None


class TestImportProgress:
    """导入进度测试。"""

    def test_import_progress_defaults(self):
        """测试导入进度默认值。"""
        progress = ImportProgress()
        assert progress.total_files == 0
        assert progress.processed_files == 0
        assert progress.status == "idle"

    def test_import_progress_calculation(self):
        """测试导入进度计算。"""
        progress = ImportProgress(
            total_files=100,
            processed_files=50
        )
        percent = int(progress.processed_files / progress.total_files * 100)
        assert percent == 50


class TestIngestionScanner:
    """内容扫描器测试。"""

    @pytest.fixture
    def mock_storage(self):
        """创建mock存储。"""
        storage = Mock()
        storage.list_files = Mock(return_value=[])
        return storage

    @pytest.fixture
    def scanner(self, mock_storage):
        """创建扫描器实例。"""
        return IngestionScanner(mock_storage)

    def test_scan_directory_empty(self, scanner, mock_storage):
        """测试扫描空目录。"""
        mock_storage.list_files.return_value = []
        
        results = scanner.scan_directory("/empty")
        assert len(results) == 0

    def test_scan_directory_with_files(self, scanner, mock_storage):
        """测试扫描包含文件的目录。"""
        mock_storage.list_files.return_value = [
            ScanResult(path="/audio/file1.mp3", name="file1.mp3", size=1000, mtime=1234567890.0, is_dir=False),
            ScanResult(path="/audio/file2.mp3", name="file2.mp3", size=2000, mtime=1234567891.0, is_dir=False),
        ]
        
        results = scanner.scan_directory("/audio", recursive=False)
        assert len(results) == 2

    def test_scan_directory_recursive(self, scanner, mock_storage):
        """测试递归扫描目录。"""
        # 第一次调用返回目录
        mock_storage.list_files.side_effect = [
            [ScanResult(path="/audio/subdir", name="subdir", size=0, mtime=0, is_dir=True)],
            [ScanResult(path="/audio/subdir/file.mp3", name="file.mp3", size=1000, mtime=1234567890.0, is_dir=False)],
        ]
        
        results = scanner.scan_directory("/audio", recursive=True)
        # 应该包含目录和文件
        assert len(results) >= 1

    def test_scan_incremental(self, scanner, mock_storage):
        """测试增量扫描。"""
        last_scan = datetime(2026, 1, 1, 0, 0, 0)
        
        mock_storage.list_files.return_value = [
            # 旧文件（修改时间在上次扫描之前）
            ScanResult(path="/audio/old.mp3", name="old.mp3", size=1000, mtime=1609459200.0, is_dir=False),  # 2021-01-01
            # 新文件（修改时间在上次扫描之后）
            ScanResult(path="/audio/new.mp3", name="new.mp3", size=2000, mtime=1798704000.0, is_dir=False),  # 2027-01-01
        ]
        
        results = scanner.scan_incremental("/audio", last_scan, recursive=False)
        # 只应该返回新文件
        assert len(results) == 1
        assert results[0].name == "new.mp3"


class TestMetadataExtractor:
    """元数据提取器测试。"""

    @pytest.fixture
    def mock_storage(self):
        """创建mock存储。"""
        storage = Mock()
        storage.read_file = Mock(return_value=b"fake audio content")
        return storage

    @pytest.fixture
    def extractor(self, mock_storage):
        """创建元数据提取器实例。"""
        return MetadataExtractor(mock_storage)

    def test_extract_metadata(self, extractor, mock_storage):
        """测试提取元数据。"""
        with patch('backend.app.services.ingestion.extract_metadata_from_bytes') as mock_extract:
            mock_extract.return_value = Mock(
                title="Test Track",
                author="Test Artist",
                duration=180.0,
                format="mp3",
                cover=None
            )
            
            metadata = extractor.extract("/audio/test.mp3", 1000, 1234567890.0)
            
            assert metadata.title == "Test Track"
            assert metadata.author == "Test Artist"
            assert metadata.duration == 180.0

    def test_extract_metadata_no_title(self, extractor, mock_storage):
        """测试提取没有标题的元数据。"""
        with patch('backend.app.services.ingestion.extract_metadata_from_bytes') as mock_extract:
            mock_extract.return_value = Mock(
                title=None,
                author=None,
                duration=None,
                format=None,
                cover=None
            )
            
            metadata = extractor.extract("/audio/test.mp3", 1000, 1234567890.0)
            
            # 应该使用文件名作为默认标题
            assert metadata.title == "test"

    def test_extract_metadata_error(self, extractor, mock_storage):
        """测试提取元数据时的错误处理。"""
        mock_storage.read_file.side_effect = Exception("Read error")
        
        metadata = extractor.extract("/audio/test.mp3", 1000, 1234567890.0)
        
        # 应该返回基本元数据
        assert metadata.title == "test"
        assert metadata.file_size == 1000


class TestImportResult:
    """导入结果测试。"""

    def test_import_result_success(self):
        """测试成功导入结果。"""
        result = ImportResult(
            success=True,
            total_files=10,
            imported_files=8,
            updated_files=2,
            skipped_files=0,
            error_files=0,
            duration_seconds=5.5,
            errors=[]
        )
        assert result.success is True
        assert result.total_files == 10
        assert result.imported_files == 8

    def test_import_result_with_errors(self):
        """测试带错误的导入结果。"""
        result = ImportResult(
            success=False,
            total_files=10,
            imported_files=5,
            updated_files=0,
            skipped_files=0,
            error_files=5,
            duration_seconds=3.0,
            errors=["Error 1", "Error 2"]
        )
        assert result.success is False
        assert result.error_files == 5
        assert len(result.errors) == 2


class TestIngestionPipelineMocked:
    """内容导入管道Mock测试。"""

    @pytest.fixture
    def mock_storage(self):
        """创建mock存储。"""
        storage = Mock()
        storage.list_files = Mock(return_value=[])
        storage.read_file = Mock(return_value=b"fake audio")
        return storage

    @pytest.fixture
    def pipeline(self, mock_storage):
        """创建导入管道实例。"""
        return IngestionPipeline(storage=mock_storage)

    def test_pipeline_initialization(self, pipeline):
        """测试管道初始化。"""
        assert pipeline.storage is not None
        assert pipeline.scanner is not None
        assert pipeline.extractor is not None
        assert pipeline.progress.status == "idle"

    def test_get_progress(self, pipeline):
        """测试获取进度。"""
        progress = pipeline.get_progress()
        assert isinstance(progress, ImportProgress)
        assert progress.status == "idle"