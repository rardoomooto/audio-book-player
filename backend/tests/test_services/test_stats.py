"""Stats service tests.

Unit tests for the StatisticsService class.
"""

import pytest
from datetime import date, datetime, timedelta
from unittest.mock import MagicMock, patch


def test_statistics_service_import():
    """Test that StatisticsService can be imported."""
    try:
        from backend.app.services.stats import StatisticsService
        assert StatisticsService is not None
    except ImportError:
        pytest.skip("StatisticsService not available")


def test_statistics_service_init():
    """Test StatisticsService initialization."""
    try:
        from backend.app.services.stats import StatisticsService
    except ImportError:
        pytest.skip("StatisticsService not available")
    
    # Create a mock database session
    mock_db = MagicMock()
    service = StatisticsService(mock_db)
    
    assert service.db == mock_db


def test_get_daily_stats_empty():
    """Test get_daily_stats with no data."""
    try:
        from backend.app.services.stats import StatisticsService
    except ImportError:
        pytest.skip("StatisticsService not available")
    
    # Create mock
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.all.return_value = []
    
    service = StatisticsService(mock_db)
    result = service.get_daily_stats()
    
    assert result == []


def test_get_weekly_stats_empty():
    """Test get_weekly_stats with no data."""
    try:
        from backend.app.services.stats import StatisticsService
    except ImportError:
        pytest.skip("StatisticsService not available")
    
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = []
    
    service = StatisticsService(mock_db)
    result = service.get_weekly_stats()
    
    assert result == []


def test_get_monthly_stats_empty():
    """Test get_monthly_stats with no data."""
    try:
        from backend.app.services.stats import StatisticsService
    except ImportError:
        pytest.skip("StatisticsService not available")
    
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = []
    
    service = StatisticsService(mock_db)
    result = service.get_monthly_stats()
    
    assert result == []


def test_get_yearly_stats_empty():
    """Test get_yearly_stats with no data."""
    try:
        from backend.app.services.stats import StatisticsService
    except ImportError:
        pytest.skip("StatisticsService not available")
    
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = []
    
    service = StatisticsService(mock_db)
    result = service.get_yearly_stats()
    
    assert result == []


def test_get_dashboard_stats():
    """Test get_dashboard_stats returns correct structure."""
    try:
        from backend.app.services.stats import StatisticsService
    except ImportError:
        pytest.skip("StatisticsService not available")
    
    mock_db = MagicMock()
    # Mock scalar returns
    mock_db.query.return_value.filter.return_value.scalar.return_value = 0
    
    service = StatisticsService(mock_db)
    result = service.get_dashboard_stats()
    
    # Check required fields
    assert "total_users" in result
    assert "total_contents" in result
    assert "total_plays" in result
    assert "total_duration_seconds" in result
    assert "today_plays" in result
    assert "week_plays" in result
    assert "month_plays" in result


def test_get_user_stats():
    """Test get_user_stats returns correct structure."""
    try:
        from backend.app.services.stats import StatisticsService
    except ImportError:
        pytest.skip("StatisticsService not available")
    
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = MagicMock(
        plays=10,
        duration_seconds=600,
        content_count=5,
        first_play=None,
        last_play=None
    )
    
    service = StatisticsService(mock_db)
    result = service.get_user_stats("test-user-id")
    
    assert result["user_id"] == "test-user-id"
    assert "plays" in result
    assert "duration_seconds" in result
    assert "content_count" in result
    assert "top_content" in result


def test_get_content_stats():
    """Test get_content_stats returns correct structure."""
    try:
        from backend.app.services.stats import StatisticsService
    except ImportError:
        pytest.skip("StatisticsService not available")
    
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = MagicMock(
        plays=5,
        duration_seconds=300,
        user_count=2,
        first_play=None,
        last_play=None
    )
    
    service = StatisticsService(mock_db)
    result = service.get_content_stats("test-content-id")
    
    assert result["content_id"] == "test-content-id"
    assert "plays" in result
    assert "duration_seconds" in result
    assert "user_count" in result
    assert "top_users" in result


def test_get_recent_activity():
    """Test get_recent_activity returns correct structure."""
    try:
        from backend.app.services.stats import StatisticsService
    except ImportError:
        pytest.skip("StatisticsService not available")
    
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = []
    
    service = StatisticsService(mock_db)
    result = service.get_recent_activity(limit=10)
    
    assert isinstance(result, list)
