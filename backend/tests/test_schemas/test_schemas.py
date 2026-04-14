"""Pydantic schema validation tests."""

import pytest
from datetime import datetime
from pydantic import ValidationError


class TestUserSchemas:
    def test_user_create_valid(self):
        from backend.app.schemas.user import UserCreate
        user = UserCreate(username="testuser", email="test@example.com", password="SecurePw1")
        assert user.username == "testuser"
        assert user.email == "test@example.com"

    def test_user_create_missing_username(self):
        from backend.app.schemas.user import UserCreate
        with pytest.raises(ValidationError):
            UserCreate(email="test@example.com", password="SecurePw1")

    def test_user_create_missing_password(self):
        from backend.app.schemas.user import UserCreate
        with pytest.raises(ValidationError):
            UserCreate(username="testuser", email="test@example.com")

    def test_user_response(self):
        from backend.app.schemas.user import UserResponse
        user = UserResponse(
            id=1,
            username="testuser",
            email="test@example.com",
            is_admin=False,
            is_active=True,
            created_at=datetime.now(),
        )
        assert user.username == "testuser"
        assert user.is_admin is False


class TestContentSchemas:
    def test_content_create_valid(self):
        from backend.app.schemas.content import ContentCreate
        content = ContentCreate(
            title="Test Book",
            path="/path/to/book.mp3",
            file_format="mp3",
        )
        assert content.title == "Test Book"
        assert content.path == "/path/to/book.mp3"

    def test_content_create_optional_fields(self):
        from backend.app.schemas.content import ContentCreate
        content = ContentCreate(
            title="Test Book",
            path="/path/to/book.mp3",
            file_format="mp3",
            author="Test Author",
            duration_seconds=3600,
        )
        assert content.author == "Test Author"
        assert content.duration_seconds == 3600

    def test_content_response(self):
        from backend.app.schemas.content import ContentResponse
        content = ContentResponse(
            content_id="abc123",
            title="Test Book",
            path="/path/to/book.mp3",
            file_format="mp3",
        )
        assert content.title == "Test Book"

    def test_folder_create(self):
        from backend.app.schemas.content import FolderCreate
        folder = FolderCreate(name="Test Folder")
        assert folder.name == "Test Folder"

    def test_folder_create_with_parent(self):
        from backend.app.schemas.content import FolderCreate
        folder = FolderCreate(name="Sub Folder", parent_id="parent-123")
        assert folder.parent_id == "parent-123"

    def test_folder_response(self):
        from backend.app.schemas.content import FolderResponse
        folder = FolderResponse(
            folder_id="folder-123",
            name="Test Folder",
            path="/test/folder",
        )
        assert folder.name == "Test Folder"


class TestLimitSchemas:
    def test_play_limit_create(self):
        from backend.app.schemas.limit import PlayLimitCreate
        limit = PlayLimitCreate(user_id=1, daily_minutes=120)
        assert limit.user_id == 1
        assert limit.daily_minutes == 120

    def test_global_limit_create(self):
        from backend.app.schemas.limit import GlobalLimitCreate
        limit = GlobalLimitCreate(daily_minutes=60)
        assert limit.daily_minutes == 60

    def test_play_limit_response(self):
        from backend.app.schemas.limit import PlayLimitResponse
        limit = PlayLimitResponse(
            id=1,
            user_id=1,
            daily_minutes=120,
            weekly_minutes=600,
            monthly_minutes=2400,
            yearly_minutes=28800,
        )
        assert limit.daily_minutes == 120


class TestPermissionSchemas:
    def test_permission_create(self):
        from backend.app.schemas.permission import PermissionCreate
        perm = PermissionCreate(user_id=1, folder_id=1, level="read")
        assert perm.user_id == 1
        assert perm.folder_id == 1
        assert perm.level == "read"

    def test_permission_response(self):
        from backend.app.schemas.permission import PermissionResponse
        perm = PermissionResponse(
            id=1,
            user_id=1,
            folder_id=1,
            level="read",
        )
        assert perm.level == "read"


class TestStatsSchemas:
    def test_daily_stat_response(self):
        from backend.app.schemas.stats import DailyStatResponse
        stat = DailyStatResponse(
            date="2026-04-01",
            total_plays=10,
            total_duration_seconds=3600,
        )
        assert stat.total_plays == 10

    def test_dashboard_stat(self):
        from backend.app.schemas.stats import DashboardStat
        stat = DashboardStat(
            total_users=5,
            total_contents=100,
            total_plays=500,
        )
        assert stat.total_users == 5
        assert stat.total_contents == 100


class TestPlaybackSchemas:
    def test_playback_request(self):
        from backend.app.schemas.playback import PlaybackRequest
        req = PlaybackRequest(content_id="content-123", position_seconds=60)
        assert req.content_id == "content-123"
        assert req.position_seconds == 60

    def test_position_update(self):
        from backend.app.schemas.playback import PositionUpdate
        pos = PositionUpdate(position_seconds=120)
        assert pos.position_seconds == 120

    def test_playback_session_response(self):
        from backend.app.schemas.playback import PlaybackSessionResponse
        session = PlaybackSessionResponse(
            session_id="session-123",
            content_id="content-123",
            position_seconds=60,
            status="playing",
        )
        assert session.status == "playing"


class TestTokenSchemas:
    def test_token_response(self):
        from backend.app.schemas.token import TokenResponse
        token = TokenResponse(
            access_token="eyJ...",
            token_type="bearer",
            expires_in=900,
        )
        assert token.token_type == "bearer"
        assert token.expires_in == 900

    def test_token_refresh_request(self):
        from backend.app.schemas.token import TokenRefreshRequest
        req = TokenRefreshRequest(refresh_token="eyJ...")
        assert req.refresh_token == "eyJ..."


class TestStorageSchemas:
    def test_file_info(self):
        from backend.app.schemas.storage import FileInfo
        info = FileInfo(
            name="test.mp3",
            path="/path/test.mp3",
            size=1024,
            mtime=1234567890.0,
            is_dir=False,
        )
        assert info.name == "test.mp3"
        assert info.is_dir is False

    def test_file_metadata(self):
        from backend.app.schemas.storage import FileMetadata
        meta = FileMetadata(
            title="Test Track",
            author="Test Artist",
            duration=180.5,
            format="mp3",
        )
        assert meta.title == "Test Track"
        assert meta.duration == 180.5

    def test_file_metadata_defaults(self):
        from backend.app.schemas.storage import FileMetadata
        meta = FileMetadata()
        assert meta.title is None
        assert meta.author is None
        assert meta.duration is None
        assert meta.format is None
        assert meta.cover is None
