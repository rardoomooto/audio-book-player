"""Scanner service unit tests."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from backend.app.services.scanner import Scanner
from backend.app.services.ingestion import ImportResult, ImportProgress


@pytest.fixture
def mock_pipeline():
    """Create a mocked ingestion pipeline."""
    pipeline = Mock()
    pipeline.run_full_import = Mock()
    pipeline.run_incremental_import = Mock()
    pipeline.get_progress = Mock()
    return pipeline


@pytest.fixture
def scanner(mock_pipeline):
    """Create a Scanner with mocked pipeline."""
    with patch("backend.app.services.scanner.get_ingestion_pipeline", return_value=mock_pipeline):
        s = Scanner()
        s._pipeline = mock_pipeline
        return s


class TestScannerInit:
    def test_scanner_has_progress(self):
        with patch("backend.app.services.scanner.get_ingestion_pipeline") as mock_get:
            mock_get.return_value = Mock()
            s = Scanner()
            assert s.progress == 0


class TestScanNas:
    def test_scan_nas_success(self, scanner, mock_pipeline):
        mock_pipeline.run_full_import.return_value = ImportResult(
            success=True,
            total_files=10,
            imported_files=10,
            updated_files=0,
            skipped_files=0,
            error_files=0,
            duration_seconds=5.0,
            errors=[],
        )

        result = scanner.scan_nas("/test/path")

        assert result["scanned"] is True
        assert result["progress"] == 100
        assert result["total_files"] == 10
        assert result["imported_files"] == 10

    def test_scan_nas_with_errors(self, scanner, mock_pipeline):
        mock_pipeline.run_full_import.return_value = ImportResult(
            success=False,
            total_files=10,
            imported_files=5,
            updated_files=0,
            skipped_files=0,
            error_files=5,
            duration_seconds=3.0,
            errors=["Error 1", "Error 2"],
        )

        result = scanner.scan_nas("/test/path")

        assert result["scanned"] is True
        assert result["progress"] == 0
        assert result["error_files"] == 5
        assert len(result["errors"]) == 2

    def test_scan_nas_exception(self, scanner, mock_pipeline):
        mock_pipeline.run_full_import.side_effect = Exception("Connection failed")

        result = scanner.scan_nas("/test/path")

        assert result["scanned"] is False
        assert result["progress"] == 0
        assert "Connection failed" in result["error"]

    def test_scan_nas_default_path(self, scanner, mock_pipeline):
        mock_pipeline.run_full_import.return_value = ImportResult(
            success=True, total_files=0, imported_files=0, updated_files=0,
            skipped_files=0, error_files=0, duration_seconds=0, errors=[],
        )

        scanner.scan_nas()

        mock_pipeline.run_full_import.assert_called_once_with("/")

    def test_scan_nas_custom_path(self, scanner, mock_pipeline):
        mock_pipeline.run_full_import.return_value = ImportResult(
            success=True, total_files=0, imported_files=0, updated_files=0,
            skipped_files=0, error_files=0, duration_seconds=0, errors=[],
        )

        scanner.scan_nas("/custom/path")

        mock_pipeline.run_full_import.assert_called_once_with("/custom/path")

    def test_scan_nas_includes_duration(self, scanner, mock_pipeline):
        mock_pipeline.run_full_import.return_value = ImportResult(
            success=True, total_files=5, imported_files=5, updated_files=0,
            skipped_files=0, error_files=0, duration_seconds=12.5, errors=[],
        )

        result = scanner.scan_nas("/test")

        assert result["duration_seconds"] == 12.5


class TestScanNasIncremental:
    def test_scan_incremental_success(self, scanner, mock_pipeline):
        mock_pipeline.run_incremental_import.return_value = ImportResult(
            success=True,
            total_files=3,
            imported_files=3,
            updated_files=0,
            skipped_files=0,
            error_files=0,
            duration_seconds=2.0,
            errors=[],
        )
        last_scan = datetime(2026, 1, 1, 0, 0, 0)

        result = scanner.scan_nas_incremental("/test", last_scan)

        assert result["scanned"] is True
        assert result["progress"] == 100
        assert result["total_files"] == 3

    def test_scan_incremental_with_errors(self, scanner, mock_pipeline):
        mock_pipeline.run_incremental_import.return_value = ImportResult(
            success=False,
            total_files=5,
            imported_files=2,
            updated_files=1,
            skipped_files=0,
            error_files=2,
            duration_seconds=4.0,
            errors=["Timeout", "Not found"],
        )
        last_scan = datetime(2026, 1, 1, 0, 0, 0)

        result = scanner.scan_nas_incremental("/test", last_scan)

        assert result["scanned"] is True
        assert result["progress"] == 0
        assert result["error_files"] == 2

    def test_scan_incremental_exception(self, scanner, mock_pipeline):
        mock_pipeline.run_incremental_import.side_effect = Exception("Disk error")
        last_scan = datetime(2026, 1, 1, 0, 0, 0)

        result = scanner.scan_nas_incremental("/test", last_scan)

        assert result["scanned"] is False
        assert result["progress"] == 0
        assert "Disk error" in result["error"]

    def test_scan_incremental_passes_last_scan_time(self, scanner, mock_pipeline):
        mock_pipeline.run_incremental_import.return_value = ImportResult(
            success=True, total_files=0, imported_files=0, updated_files=0,
            skipped_files=0, error_files=0, duration_seconds=0, errors=[],
        )
        last_scan = datetime(2026, 3, 15, 12, 30, 0)

        scanner.scan_nas_incremental("/test", last_scan)

        mock_pipeline.run_incremental_import.assert_called_once_with("/test", last_scan)


class TestGetScanProgress:
    def test_get_progress_with_files(self, scanner, mock_pipeline):
        mock_pipeline.get_progress.return_value = ImportProgress(
            total_files=100,
            processed_files=50,
            success_count=45,
            error_count=5,
            current_file="/audio/chapter5.mp3",
            status="importing",
        )

        result = scanner.get_scan_progress()

        assert result["status"] == "importing"
        assert result["total_files"] == 100
        assert result["processed_files"] == 50
        assert result["success_count"] == 45
        assert result["error_count"] == 5
        assert result["current_file"] == "/audio/chapter5.mp3"
        assert result["progress_percent"] == 50

    def test_get_progress_zero_total(self, scanner, mock_pipeline):
        mock_pipeline.get_progress.return_value = ImportProgress(
            total_files=0,
            processed_files=0,
            success_count=0,
            error_count=0,
            current_file="",
            status="idle",
        )

        result = scanner.get_scan_progress()

        assert result["progress_percent"] == 0
        assert result["status"] == "idle"

    def test_get_progress_complete(self, scanner, mock_pipeline):
        mock_pipeline.get_progress.return_value = ImportProgress(
            total_files=20,
            processed_files=20,
            success_count=20,
            error_count=0,
            current_file="/audio/chapter20.mp3",
            status="completed",
        )

        result = scanner.get_scan_progress()

        assert result["progress_percent"] == 100
        assert result["status"] == "completed"

    def test_get_progress_partial_percent(self, scanner, mock_pipeline):
        mock_pipeline.get_progress.return_value = ImportProgress(
            total_files=7,
            processed_files=3,
            success_count=3,
            error_count=0,
            current_file="",
            status="importing",
        )

        result = scanner.get_scan_progress()

        assert result["progress_percent"] == 42
