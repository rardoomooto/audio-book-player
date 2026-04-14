"""Token黑名单服务单元测试。"""

import time
import pytest
from backend.app.services.token_blacklist import (
    blacklist_token,
    is_token_blacklisted,
    cleanup_expired,
    _blacklist,
)


class TestTokenBlacklist:
    """Token黑名单测试。"""

    @pytest.fixture(autouse=True)
    def clear_blacklist(self):
        """每个测试前清空黑名单。"""
        _blacklist.clear()
        yield
        _blacklist.clear()

    def test_blacklist_token(self):
        """测试将token加入黑名单。"""
        blacklist_token("jti123", int(time.time()) + 3600)
        assert "jti123" in _blacklist

    def test_is_token_blacklisted_true(self):
        """测试token在黑名单中。"""
        future_ts = int(time.time()) + 3600
        blacklist_token("jti123", future_ts)
        
        assert is_token_blacklisted("jti123") is True

    def test_is_token_blacklisted_false_not_in_list(self):
        """测试token不在黑名单中。"""
        assert is_token_blacklisted("nonexistent") is False

    def test_is_token_blacklisted_expired(self):
        """测试过期的token返回False。"""
        past_ts = int(time.time()) - 100
        blacklist_token("jti123", past_ts)
        
        assert is_token_blacklisted("jti123") is False

    def test_is_token_blacklisted_removes_expired(self):
        """测试检查时自动移除过期token。"""
        past_ts = int(time.time()) - 100
        blacklist_token("jti123", past_ts)
        
        is_token_blacklisted("jti123")
        assert "jti123" not in _blacklist

    def test_cleanup_expired(self):
        """测试清理过期token。"""
        past_ts = int(time.time()) - 100
        future_ts = int(time.time()) + 3600
        
        blacklist_token("expired1", past_ts)
        blacklist_token("expired2", past_ts)
        blacklist_token("valid", future_ts)
        
        cleanup_expired()
        
        assert "expired1" not in _blacklist
        assert "expired2" not in _blacklist
        assert "valid" in _blacklist

    def test_multiple_tokens(self):
        """测试多个token的黑名单管理。"""
        future_ts = int(time.time()) + 3600
        
        blacklist_token("jti1", future_ts)
        blacklist_token("jti2", future_ts)
        blacklist_token("jti3", future_ts)
        
        assert is_token_blacklisted("jti1") is True
        assert is_token_blacklisted("jti2") is True
        assert is_token_blacklisted("jti3") is True

    def test_overwrite_blacklist_entry(self):
        """测试覆盖已有的黑名单条目。"""
        ts1 = int(time.time()) + 1000
        ts2 = int(time.time()) + 2000
        
        blacklist_token("jti123", ts1)
        blacklist_token("jti123", ts2)
        
        assert _blacklist["jti123"] == ts2
