"""播放服务。

提供播放会话管理、进度跟踪和时长限制功能。
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class PlaybackState(str, Enum):
    """播放状态枚举。"""
    IDLE = "idle"
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"


@dataclass
class PlaybackSession:
    """播放会话。"""
    session_id: str
    user_id: str
    content_id: str
    state: PlaybackState
    position_seconds: int
    start_time: datetime
    last_update_time: datetime
    duration_seconds: int = 0


@dataclass
class PlayLimit:
    """播放限制。"""
    user_id: Optional[str]
    daily_minutes: int = 0
    weekly_minutes: Optional[int] = None
    monthly_minutes: Optional[int] = None
    yearly_minutes: Optional[int] = None


class PlaybackService:
    """播放服务。
    
    管理播放会话、进度跟踪和时长限制。
    """
    
    def __init__(self):
        # 活跃的播放会话：session_id -> PlaybackSession
        self._sessions: Dict[str, PlaybackSession] = {}
        # 用户播放限制：user_id -> PlayLimit
        self._limits: Dict[str, PlayLimit] = {}
        # 全局默认限制
        self._global_limit: PlayLimit = PlayLimit(user_id=None, daily_minutes=60)
        # 播放记录：user_id -> List[Dict]
        self._play_records: Dict[str, List[Dict[str, Any]]] = {}
    
    def start_playback(self, user_id: str, content_id: str, position_seconds: int = 0) -> Dict[str, Any]:
        """开始播放。
        
        Args:
            user_id: 用户ID
            content_id: 内容ID
            position_seconds: 起始位置（秒）
            
        Returns:
            Dict[str, Any]: 播放会话信息
            
        Raises:
            ValueError: 超过播放限制
        """
        # 检查播放限制
        self._check_play_limit(user_id)
        
        # 停止用户当前的播放会话
        self._stop_user_sessions(user_id)
        
        # 创建新的播放会话
        session_id = f"{user_id}_{content_id}_{datetime.utcnow().timestamp()}"
        session = PlaybackSession(
            session_id=session_id,
            user_id=user_id,
            content_id=content_id,
            state=PlaybackState.PLAYING,
            position_seconds=position_seconds,
            start_time=datetime.utcnow(),
            last_update_time=datetime.utcnow(),
        )
        
        self._sessions[session_id] = session
        
        logger.info(f"开始播放: 用户={user_id}, 内容={content_id}, 位置={position_seconds}秒")
        
        return self._session_to_dict(session)
    
    def pause_playback(self, user_id: str, content_id: str) -> Dict[str, Any]:
        """暂停播放。
        
        Args:
            user_id: 用户ID
            content_id: 内容ID
            
        Returns:
            Dict[str, Any]: 更新后的播放会话信息
        """
        session = self._get_user_session(user_id, content_id)
        if not session:
            raise ValueError("播放会话不存在")
        
        session.state = PlaybackState.PAUSED
        session.last_update_time = datetime.utcnow()
        
        # 记录播放时长
        self._record_play_duration(user_id, session)
        
        logger.info(f"暂停播放: 用户={user_id}, 内容={content_id}")
        
        return self._session_to_dict(session)
    
    def resume_playback(self, user_id: str, content_id: str) -> Dict[str, Any]:
        """恢复播放。
        
        Args:
            user_id: 用户ID
            content_id: 内容ID
            
        Returns:
            Dict[str, Any]: 更新后的播放会话信息
        """
        session = self._get_user_session(user_id, content_id)
        if not session:
            raise ValueError("播放会话不存在")
        
        # 检查播放限制
        self._check_play_limit(user_id)
        
        session.state = PlaybackState.PLAYING
        session.last_update_time = datetime.utcnow()
        
        logger.info(f"恢复播放: 用户={user_id}, 内容={content_id}")
        
        return self._session_to_dict(session)
    
    def stop_playback(self, user_id: str, content_id: str) -> Dict[str, Any]:
        """停止播放。
        
        Args:
            user_id: 用户ID
            content_id: 内容ID
            
        Returns:
            Dict[str, Any]: 停止的播放会话信息
        """
        session = self._get_user_session(user_id, content_id)
        if not session:
            raise ValueError("播放会话不存在")
        
        session.state = PlaybackState.STOPPED
        session.last_update_time = datetime.utcnow()
        
        # 记录播放时长
        self._record_play_duration(user_id, session)
        
        # 从活跃会话中移除
        del self._sessions[session.session_id]
        
        logger.info(f"停止播放: 用户={user_id}, 内容={content_id}")
        
        return self._session_to_dict(session)
    
    def update_position(self, user_id: str, content_id: str, position_seconds: int) -> Dict[str, Any]:
        """更新播放位置。
        
        Args:
            user_id: 用户ID
            content_id: 内容ID
            position_seconds: 新位置（秒）
            
        Returns:
            Dict[str, Any]: 更新后的播放会话信息
        """
        session = self._get_user_session(user_id, content_id)
        if not session:
            raise ValueError("播放会话不存在")
        
        # 检查播放限制（如果正在播放）
        if session.state == PlaybackState.PLAYING:
            self._check_play_limit(user_id)
        
        session.position_seconds = position_seconds
        session.last_update_time = datetime.utcnow()
        
        logger.info(f"更新播放位置: 用户={user_id}, 内容={content_id}, 位置={position_seconds}秒")
        
        return self._session_to_dict(session)
    
    def get_current_playback(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户当前播放状态。
        
        Args:
            user_id: 用户ID
            
        Returns:
            Optional[Dict[str, Any]]: 当前播放会话信息，如果没有则返回None
        """
        for session in self._sessions.values():
            if session.user_id == user_id and session.state != PlaybackState.STOPPED:
                return self._session_to_dict(session)
        return None
    
    def get_playback_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """获取播放会话信息。
        
        Args:
            session_id: 会话ID
            
        Returns:
            Optional[Dict[str, Any]]: 播放会话信息，如果不存在则返回None
        """
        session = self._sessions.get(session_id)
        if session:
            return self._session_to_dict(session)
        return None
    
    def set_play_limit(self, user_id: Optional[str], daily_minutes: int, 
                      weekly_minutes: Optional[int] = None,
                      monthly_minutes: Optional[int] = None,
                      yearly_minutes: Optional[int] = None) -> None:
        """设置播放限制。
        
        Args:
            user_id: 用户ID（None表示全局限制）
            daily_minutes: 每日限制分钟数
            weekly_minutes: 每周限制分钟数
            monthly_minutes: 每月限制分钟数
            yearly_minutes: 每年限制分钟数
        """
        limit = PlayLimit(
            user_id=user_id,
            daily_minutes=daily_minutes,
            weekly_minutes=weekly_minutes,
            monthly_minutes=monthly_minutes,
            yearly_minutes=yearly_minutes,
        )
        
        if user_id is None:
            self._global_limit = limit
            logger.info(f"更新全局播放限制: 每日={daily_minutes}分钟")
        else:
            self._limits[user_id] = limit
            logger.info(f"更新用户播放限制: 用户={user_id}, 每日={daily_minutes}分钟")
    
    def get_play_limit(self, user_id: Optional[str]) -> Dict[str, Any]:
        """获取用户播放限制。

        Args:
            user_id: 用户ID，None表示获取全局限制

        Returns:
            Dict[str, Any]: 播放限制信息
        """
        if user_id is None:
            return self._limit_to_dict(self._global_limit)
        user_limit = self._limits.get(user_id)
        if user_limit:
            return self._limit_to_dict(user_limit)
        return self._limit_to_dict(self._global_limit)
    
    def get_today_play_time(self, user_id: str) -> int:
        """获取用户今日播放时长（分钟）。
        
        Args:
            user_id: 用户ID
            
        Returns:
            int: 今日播放时长（分钟）
        """
        today = datetime.utcnow().date()
        records = self._play_records.get(user_id, [])
        
        total_seconds = 0
        for record in records:
            record_date = record.get("date")
            if record_date and record_date.date() == today:
                total_seconds += record.get("duration_seconds", 0)
        
        return total_seconds // 60
    
    def _check_play_limit(self, user_id: str) -> None:
        """检查播放限制。
        
        Args:
            user_id: 用户ID
            
        Raises:
            ValueError: 超过播放限制
        """
        limit = self._limits.get(user_id) or self._global_limit
        
        if limit.daily_minutes and limit.daily_minutes > 0:
            today_minutes = self.get_today_play_time(user_id)
            if today_minutes >= limit.daily_minutes:
                raise ValueError(f"超过每日播放限制: {limit.daily_minutes}分钟")
    
    def _stop_user_sessions(self, user_id: str) -> None:
        """停止用户的所有播放会话。
        
        Args:
            user_id: 用户ID
        """
        sessions_to_remove = []
        for session_id, session in self._sessions.items():
            if session.user_id == user_id:
                session.state = PlaybackState.STOPPED
                session.last_update_time = datetime.utcnow()
                self._record_play_duration(user_id, session)
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self._sessions[session_id]
    
    def _get_user_session(self, user_id: str, content_id: str) -> Optional[PlaybackSession]:
        """获取用户的播放会话。
        
        Args:
            user_id: 用户ID
            content_id: 内容ID
            
        Returns:
            Optional[PlaybackSession]: 播放会话，如果不存在则返回None
        """
        for session in self._sessions.values():
            if session.user_id == user_id and session.content_id == content_id:
                return session
        return None
    
    def _record_play_duration(self, user_id: str, session: PlaybackSession) -> None:
        """记录播放时长。
        
        Args:
            user_id: 用户ID
            session: 播放会话
        """
        now = datetime.utcnow()
        duration = (now - session.last_update_time).total_seconds()
        
        if duration > 0:
            if user_id not in self._play_records:
                self._play_records[user_id] = []
            
            self._play_records[user_id].append({
                "date": now,
                "duration_seconds": int(duration),
                "content_id": session.content_id,
                "position_seconds": session.position_seconds,
            })
    
    def _session_to_dict(self, session: PlaybackSession) -> Dict[str, Any]:
        """将会话转换为字典。
        
        Args:
            session: 播放会话
            
        Returns:
            Dict[str, Any]: 会话字典
        """
        return {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "content_id": session.content_id,
            "state": session.state.value,
            "position_seconds": session.position_seconds,
            "start_time": session.start_time.isoformat(),
            "last_update_time": session.last_update_time.isoformat(),
            "duration_seconds": session.duration_seconds,
        }
    
    def _limit_to_dict(self, limit: PlayLimit) -> Dict[str, Any]:
        """将限制转换为字典。
        
        Args:
            limit: 播放限制
            
        Returns:
            Dict[str, Any]: 限制字典
        """
        return {
            "user_id": limit.user_id,
            "daily_minutes": limit.daily_minutes,
            "weekly_minutes": limit.weekly_minutes,
            "monthly_minutes": limit.monthly_minutes,
            "yearly_minutes": limit.yearly_minutes,
        }


# 全局播放服务实例
_playback_service: Optional[PlaybackService] = None


def get_playback_service() -> PlaybackService:
    """获取播放服务实例。
    
    Returns:
        PlaybackService: 播放服务实例
    """
    global _playback_service
    if _playback_service is None:
        _playback_service = PlaybackService()
    return _playback_service