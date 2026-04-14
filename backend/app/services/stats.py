"""统计服务。

提供播放统计收集、聚合和查询功能。
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from typing import Optional, List, Dict, Any
from collections import defaultdict
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from backend.app.models.playback import PlayRecord
from backend.app.models.user import User
from backend.app.models.content import Content

logger = logging.getLogger(__name__)


class StatisticsService:
    """统计服务。
    
    提供播放记录的聚合和查询功能。
    """
    
    def __init__(self, db: Session):
        """初始化统计服务。
        
        Args:
            db: 数据库会话
        """
        self.db = db
    
    def get_daily_stats(
        self,
        user_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 30,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """获取每日统计。
        
        Args:
            user_id: 用户ID（可选）
            start_date: 开始日期
            end_date: 结束日期
            limit: 返回数量限制
            offset: 偏移量
            
        Returns:
            List[Dict]: 每日统计列表
        """
        query = self.db.query(
            func.date(PlayRecord.start_time).label('date'),
            func.count(PlayRecord.record_id).label('plays'),
            func.coalesce(func.sum(PlayRecord.duration_seconds), 0).label('duration_seconds'),
            func.count(func.distinct(PlayRecord.content_id)).label('content_count')
        )
        
        # 应用过滤条件
        filters = []
        if user_id:
            filters.append(PlayRecord.user_id == user_id)
        if start_date:
            filters.append(func.date(PlayRecord.start_time) >= start_date)
        if end_date:
            filters.append(func.date(PlayRecord.start_time) <= end_date)
            
        if filters:
            query = query.filter(and_(*filters))
            
        # 按日期分组和排序
        results = query.group_by(
            func.date(PlayRecord.start_time)
        ).order_by(
            func.date(PlayRecord.start_time).desc()
        ).limit(limit).offset(offset).all()
        
        return [
            {
                "date": str(r.date),
                "plays": r.plays,
                "duration_seconds": r.duration_seconds,
                "content_count": r.content_count
            }
            for r in results
        ]
    
    def get_weekly_stats(
        self,
        user_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 52
    ) -> List[Dict[str, Any]]:
        """获取每周统计。
        
        Args:
            user_id: 用户ID（可选）
            start_date: 开始日期
            end_date: 结束日期
            limit: 返回数量限制
            
        Returns:
            List[Dict]: 每周统计列表
        """
        # 使用strftime获取周数
        query = self.db.query(
            func.strftime('%Y-W%W', PlayRecord.start_time).label('week'),
            func.count(PlayRecord.record_id).label('plays'),
            func.coalesce(func.sum(PlayRecord.duration_seconds), 0).label('duration_seconds'),
            func.count(func.distinct(PlayRecord.content_id)).label('content_count')
        )
        
        # 应用过滤条件
        filters = []
        if user_id:
            filters.append(PlayRecord.user_id == user_id)
        if start_date:
            filters.append(func.date(PlayRecord.start_time) >= start_date)
        if end_date:
            filters.append(func.date(PlayRecord.start_time) <= end_date)
            
        if filters:
            query = query.filter(and_(*filters))
            
        results = query.group_by(
            func.strftime('%Y-W%W', PlayRecord.start_time)
        ).order_by(
            func.strftime('%Y-W%W', PlayRecord.start_time).desc()
        ).limit(limit).all()
        
        return [
            {
                "date": r.week,
                "plays": r.plays,
                "duration_seconds": r.duration_seconds,
                "content_count": r.content_count
            }
            for r in results
        ]
    
    def get_monthly_stats(
        self,
        user_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 24
    ) -> List[Dict[str, Any]]:
        """获取每月统计。
        
        Args:
            user_id: 用户ID（可选）
            start_date: 开始日期
            end_date: 结束日期
            limit: 返回数量限制
            
        Returns:
            List[Dict]: 每月统计列表
        """
        query = self.db.query(
            func.strftime('%Y-%m', PlayRecord.start_time).label('month'),
            func.count(PlayRecord.record_id).label('plays'),
            func.coalesce(func.sum(PlayRecord.duration_seconds), 0).label('duration_seconds'),
            func.count(func.distinct(PlayRecord.content_id)).label('content_count')
        )
        
        # 应用过滤条件
        filters = []
        if user_id:
            filters.append(PlayRecord.user_id == user_id)
        if start_date:
            filters.append(func.date(PlayRecord.start_time) >= start_date)
        if end_date:
            filters.append(func.date(PlayRecord.start_time) <= end_date)
            
        if filters:
            query = query.filter(and_(*filters))
            
        results = query.group_by(
            func.strftime('%Y-%m', PlayRecord.start_time)
        ).order_by(
            func.strftime('%Y-%m', PlayRecord.start_time).desc()
        ).limit(limit).all()
        
        return [
            {
                "date": r.month,
                "plays": r.plays,
                "duration_seconds": r.duration_seconds,
                "content_count": r.content_count
            }
            for r in results
        ]
    
    def get_yearly_stats(
        self,
        user_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """获取每年统计。
        
        Args:
            user_id: 用户ID（可选）
            limit: 返回数量限制
            
        Returns:
            List[Dict]: 每年统计列表
        """
        query = self.db.query(
            func.strftime('%Y', PlayRecord.start_time).label('year'),
            func.count(PlayRecord.record_id).label('plays'),
            func.coalesce(func.sum(PlayRecord.duration_seconds), 0).label('duration_seconds'),
            func.count(func.distinct(PlayRecord.content_id)).label('content_count')
        )
        
        # 应用过滤条件
        filters = []
        if user_id:
            filters.append(PlayRecord.user_id == user_id)
            
        if filters:
            query = query.filter(and_(*filters))
            
        results = query.group_by(
            func.strftime('%Y', PlayRecord.start_time)
        ).order_by(
            func.strftime('%Y', PlayRecord.start_time).desc()
        ).limit(limit).all()
        
        return [
            {
                "date": r.year,
                "plays": r.plays,
                "duration_seconds": r.duration_seconds,
                "content_count": r.content_count
            }
            for r in results
        ]
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """获取用户统计。
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 用户统计信息
        """
        result = self.db.query(
            func.count(PlayRecord.record_id).label('plays'),
            func.coalesce(func.sum(PlayRecord.duration_seconds), 0).label('duration_seconds'),
            func.count(func.distinct(PlayRecord.content_id)).label('content_count'),
            func.min(PlayRecord.start_time).label('first_play'),
            func.max(PlayRecord.start_time).label('last_play')
        ).filter(PlayRecord.user_id == user_id).first()
        
        # 处理可能的None值
        plays = result.plays if result and result.plays is not None else 0
        duration = result.duration_seconds if result and result.duration_seconds is not None else 0
        content_cnt = result.content_count if result and result.content_count is not None else 0
        first_play = result.first_play if result and result.first_play else None
        last_play = result.last_play if result and result.last_play else None
        
        # 获取最常播放的内容
        top_content = self.db.query(
            PlayRecord.content_id,
            func.count(PlayRecord.record_id).label('play_count'),
            func.coalesce(func.sum(PlayRecord.duration_seconds), 0).label('total_duration')
        ).filter(
            PlayRecord.user_id == user_id
        ).group_by(
            PlayRecord.content_id
        ).order_by(
            func.sum(PlayRecord.duration_seconds).desc()
        ).limit(5).all()
        
        return {
            "user_id": user_id,
            "plays": plays,
            "duration_seconds": duration,
            "content_count": content_cnt,
            "first_play": first_play.isoformat() if first_play else None,
            "last_play": last_play.isoformat() if last_play else None,
            "top_content": [
                {
                    "content_id": tc.content_id,
                    "play_count": tc.play_count,
                    "total_duration": tc.total_duration
                }
                for tc in top_content
            ]
        }
    
    def get_content_stats(self, content_id: str) -> Dict[str, Any]:
        """获取内容统计。
        
        Args:
            content_id: 内容ID
            
        Returns:
            Dict: 内容统计信息
        """
        result = self.db.query(
            func.count(PlayRecord.record_id).label('plays'),
            func.coalesce(func.sum(PlayRecord.duration_seconds), 0).label('duration_seconds'),
            func.count(func.distinct(PlayRecord.user_id)).label('user_count'),
            func.min(PlayRecord.start_time).label('first_play'),
            func.max(PlayRecord.start_time).label('last_play')
        ).filter(PlayRecord.content_id == content_id).first()
        
        # 处理可能的None值
        plays = result.plays if result and result.plays is not None else 0
        duration = result.duration_seconds if result and result.duration_seconds is not None else 0
        user_cnt = result.user_count if result and result.user_count is not None else 0
        first_play = result.first_play if result and result.first_play else None
        last_play = result.last_play if result and result.last_play else None
        
        # 获取播放最多的用户
        top_users = self.db.query(
            PlayRecord.user_id,
            func.count(PlayRecord.record_id).label('play_count'),
            func.coalesce(func.sum(PlayRecord.duration_seconds), 0).label('total_duration')
        ).filter(
            PlayRecord.content_id == content_id
        ).group_by(
            PlayRecord.user_id
        ).order_by(
            func.sum(PlayRecord.duration_seconds).desc()
        ).limit(5).all()
        
        return {
            "content_id": content_id,
            "plays": plays,
            "duration_seconds": duration,
            "user_count": user_cnt,
            "first_play": first_play.isoformat() if first_play else None,
            "last_play": last_play.isoformat() if last_play else None,
            "top_users": [
                {
                    "user_id": tu.user_id,
                    "play_count": tu.play_count,
                    "total_duration": tu.total_duration
                }
                for tu in top_users
            ]
        }
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """获取仪表板统计。
        
        Returns:
            Dict: 仪表板统计数据
        """
        # 总用户数
        total_users = self.db.query(func.count(User.user_id)).scalar() or 0
        
        # 总内容数
        total_contents = self.db.query(func.count(Content.content_id)).scalar() or 0
        
        # 总播放次数
        total_plays = self.db.query(func.count(PlayRecord.record_id)).scalar() or 0
        
        # 总播放时长
        total_duration = self.db.query(
            func.coalesce(func.sum(PlayRecord.duration_seconds), 0)
        ).scalar() or 0
        
        # 今日播放次数
        today = datetime.now().date()
        today_str = today.isoformat()
        today_plays = self.db.query(func.count(PlayRecord.record_id)).filter(
            func.date(PlayRecord.start_time) == today_str
        ).scalar() or 0
        
        # 今日播放时长
        today_duration = self.db.query(
            func.coalesce(func.sum(PlayRecord.duration_seconds), 0)
        ).filter(func.date(PlayRecord.start_time) == today_str).scalar() or 0
        
        # 本周播放次数
        week_start = today - timedelta(days=today.weekday())
        week_str = week_start.isoformat()
        week_plays = self.db.query(func.count(PlayRecord.record_id)).filter(
            func.date(PlayRecord.start_time) >= week_str
        ).scalar() or 0
        
        # 本月播放次数
        month_start = today.replace(day=1)
        month_str = month_start.isoformat()
        month_plays = self.db.query(func.count(PlayRecord.record_id)).filter(
            func.date(PlayRecord.start_time) >= month_str
        ).scalar() or 0
        
        return {
            "total_users": total_users,
            "total_contents": total_contents,
            "total_plays": total_plays,
            "total_duration_seconds": total_duration,
            "today_plays": today_plays,
            "today_duration_seconds": today_duration,
            "week_plays": week_plays,
            "month_plays": month_plays
        }
    
    def get_recent_activity(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取最近活动。
        
        Args:
            limit: 返回数量限制
            
        Returns:
            List[Dict]: 最近活动列表
        """
        results = self.db.query(
            PlayRecord
        ).order_by(
            PlayRecord.start_time.desc()
        ).limit(limit).all()
        
        activities = []
        for r in results:
            # 获取用户名和内容名
            user = self.db.query(User).filter(User.user_id == r.user_id).first()
            content = self.db.query(Content).filter(Content.content_id == r.content_id).first()
            
            # 获取实际的时间值
            start_time_val = r.start_time
            if hasattr(start_time_val, 'isoformat'):
                start_time_str = start_time_val.isoformat()
            else:
                start_time_str = None
            
            activities.append({
                "record_id": r.record_id,
                "user_id": r.user_id,
                "user_name": user.username if user else "Unknown",
                "content_id": r.content_id,
                "content_title": content.title if content else "Unknown",
                "start_time": start_time_str,
                "duration_seconds": r.duration_seconds or 0,
                "action": "play"
            })
        
        return activities
