"""播放服务单元测试。"""

import pytest
from datetime import datetime, timedelta
from backend.app.services.playback import (
    PlaybackService,
    PlaybackState,
    PlaybackSession,
    PlayLimit,
    get_playback_service,
)


class TestPlaybackService:
    """播放服务测试。"""

    @pytest.fixture
    def service(self):
        """创建播放服务实例。"""
        return PlaybackService()

    def test_start_playback(self, service):
        """测试开始播放。"""
        result = service.start_playback("user1", "content1", 0)
        assert result["user_id"] == "user1"
        assert result["content_id"] == "content1"
        assert result["state"] == PlaybackState.PLAYING.value
        assert result["position_seconds"] == 0

    def test_start_playback_with_position(self, service):
        """测试从指定位置开始播放。"""
        result = service.start_playback("user1", "content1", 300)
        assert result["position_seconds"] == 300

    def test_pause_playback(self, service):
        """测试暂停播放。"""
        service.start_playback("user1", "content1", 0)
        result = service.pause_playback("user1", "content1")
        assert result["state"] == PlaybackState.PAUSED.value

    def test_pause_nonexistent_session(self, service):
        """测试暂停不存在的会话。"""
        with pytest.raises(ValueError, match="播放会话不存在"):
            service.pause_playback("user1", "content1")

    def test_resume_playback(self, service):
        """测试恢复播放。"""
        service.start_playback("user1", "content1", 0)
        service.pause_playback("user1", "content1")
        result = service.resume_playback("user1", "content1")
        assert result["state"] == PlaybackState.PLAYING.value

    def test_resume_nonexistent_session(self, service):
        """测试恢复不存在的会话。"""
        with pytest.raises(ValueError, match="播放会话不存在"):
            service.resume_playback("user1", "content1")

    def test_stop_playback(self, service):
        """测试停止播放。"""
        service.start_playback("user1", "content1", 0)
        result = service.stop_playback("user1", "content1")
        assert result["state"] == PlaybackState.STOPPED.value

        # 验证会话已被移除
        current = service.get_current_playback("user1")
        assert current is None

    def test_stop_nonexistent_session(self, service):
        """测试停止不存在的会话。"""
        with pytest.raises(ValueError, match="播放会话不存在"):
            service.stop_playback("user1", "content1")

    def test_update_position(self, service):
        """测试更新播放位置。"""
        service.start_playback("user1", "content1", 0)
        result = service.update_position("user1", "content1", 500)
        assert result["position_seconds"] == 500

    def test_get_current_playback(self, service):
        """测试获取当前播放状态。"""
        service.start_playback("user1", "content1", 100)
        current = service.get_current_playback("user1")
        assert current is not None
        assert current["content_id"] == "content1"
        assert current["position_seconds"] == 100

    def test_get_current_playback_no_session(self, service):
        """测试获取没有播放会话的用户状态。"""
        current = service.get_current_playback("user1")
        assert current is None

    def test_get_playback_session(self, service):
        """测试获取播放会话。"""
        result = service.start_playback("user1", "content1", 0)
        session_id = result["session_id"]
        
        session = service.get_playback_session(session_id)
        assert session is not None
        assert session["session_id"] == session_id

    def test_get_nonexistent_session(self, service):
        """测试获取不存在的会话。"""
        session = service.get_playback_session("nonexistent")
        assert session is None

    def test_start_new_session_stops_old(self, service):
        """测试开始新会话时停止旧会话。"""
        service.start_playback("user1", "content1", 0)
        service.start_playback("user1", "content2", 0)
        
        # 验证只有新会话存在
        current = service.get_current_playback("user1")
        assert current["content_id"] == "content2"


class TestPlayLimits:
    """播放限制测试。"""

    @pytest.fixture
    def service(self):
        """创建播放服务实例。"""
        svc = PlaybackService()
        # 设置一个较小的限制便于测试
        svc.set_play_limit(None, daily_minutes=1)
        return svc

    def test_set_global_limit(self, service):
        """测试设置全局限制。"""
        service.set_play_limit(None, daily_minutes=120)
        limit = service.get_play_limit("any_user")
        assert limit["daily_minutes"] == 120

    def test_set_user_limit(self, service):
        """测试设置用户限制。"""
        service.set_play_limit("user1", daily_minutes=30)
        limit = service.get_play_limit("user1")
        assert limit["daily_minutes"] == 30

    def test_user_limit_overrides_global(self, service):
        """测试用户限制覆盖全局限制。"""
        service.set_play_limit(None, daily_minutes=60)
        service.set_play_limit("user1", daily_minutes=30)
        
        limit1 = service.get_play_limit("user1")
        limit2 = service.get_play_limit("user2")
        
        assert limit1["daily_minutes"] == 30
        assert limit2["daily_minutes"] == 60

    def test_play_limit_check(self, service):
        """测试播放限制检查。"""
        # 设置限制为1分钟
        service.set_play_limit("user1", daily_minutes=1)
        
        # 开始播放应该成功
        service.start_playback("user1", "content1", 0)
        
        # 模拟播放时间超过限制
        service._play_records["user1"] = [
            {"date": datetime.utcnow(), "duration_seconds": 120, "content_id": "content1"}
        ]
        
        # 尝试再次播放应该失败
        with pytest.raises(ValueError, match="超过每日播放限制"):
            service.start_playback("user1", "content2", 0)

    def test_get_today_play_time(self, service):
        """测试获取今日播放时长。"""
        # 添加播放记录
        service._play_records["user1"] = [
            {"date": datetime.utcnow(), "duration_seconds": 300},  # 5分钟
            {"date": datetime.utcnow(), "duration_seconds": 600},  # 10分钟
        ]
        
        minutes = service.get_today_play_time("user1")
        assert minutes == 15  # 15分钟

    def test_get_today_play_time_empty(self, service):
        """测试获取没有播放记录的今日时长。"""
        minutes = service.get_today_play_time("user1")
        assert minutes == 0


class TestPlaybackServiceSingleton:
    """播放服务单例测试。"""

    def test_get_playback_service_singleton(self):
        """测试获取播放服务单例。"""
        service1 = get_playback_service()
        service2 = get_playback_service()
        assert service1 is service2