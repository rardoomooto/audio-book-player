"""测试数据工厂 - Stats模型。"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import random


class StatsFactory:
    """统计数据工厂类。"""

    _next_id = 1

    @classmethod
    def create_daily_stats(cls, **kwargs) -> Dict[str, Any]:
        """创建每日统计数据。

        Args:
            user_id: 用户ID
            date: 日期（默认今天）
            total_duration_seconds: 总播放时长（秒）
            content_count: 播放内容数量
            most_played_content_id: 最常播放内容ID

        Returns:
            Dict[str, Any]: 每日统计数据
        """
        stats_id = kwargs.get("id", cls._next_id)
        cls._next_id += 1

        return {
            "id": stats_id,
            "user_id": kwargs.get("user_id", 1),
            "date": kwargs.get("date", datetime.utcnow().date().isoformat()),
            "total_duration_seconds": kwargs.get("total_duration_seconds", random.randint(600, 7200)),
            "content_count": kwargs.get("content_count", random.randint(1, 10)),
            "most_played_content_id": kwargs.get("most_played_content_id", 1),
            "created_at": kwargs.get("created_at", datetime.utcnow().isoformat()),
            "updated_at": kwargs.get("updated_at", datetime.utcnow().isoformat()),
        }

    @classmethod
    def create_weekly_stats(cls, **kwargs) -> Dict[str, Any]:
        """创建每周统计数据。"""
        start_date = kwargs.get("start_date", datetime.utcnow().date() - timedelta(days=7))
        
        return {
            "user_id": kwargs.get("user_id", 1),
            "week_start": start_date.isoformat() if hasattr(start_date, 'isoformat') else str(start_date),
            "total_duration_seconds": kwargs.get("total_duration_seconds", random.randint(3600, 50400)),
            "content_count": kwargs.get("content_count", random.randint(5, 50)),
            "sessions_count": kwargs.get("sessions_count", random.randint(5, 20)),
        }

    @classmethod
    def create_monthly_stats(cls, **kwargs) -> Dict[str, Any]:
        """创建每月统计数据。"""
        return {
            "user_id": kwargs.get("user_id", 1),
            "month": kwargs.get("month", datetime.utcnow().strftime("%Y-%m")),
            "total_duration_seconds": kwargs.get("total_duration_seconds", random.randint(7200, 216000)),
            "content_count": kwargs.get("content_count", random.randint(10, 100)),
            "sessions_count": kwargs.get("sessions_count", random.randint(20, 80)),
        }

    @classmethod
    def create_yearly_stats(cls, **kwargs) -> Dict[str, Any]:
        """创建每年统计数据。"""
        return {
            "user_id": kwargs.get("user_id", 1),
            "year": kwargs.get("year", datetime.utcnow().year),
            "total_duration_seconds": kwargs.get("total_duration_seconds", random.randint(86400, 2592000)),
            "content_count": kwargs.get("content_count", random.randint(50, 500)),
            "sessions_count": kwargs.get("sessions_count", random.randint(100, 500)),
        }

    @classmethod
    def create_dashboard_stats(cls, **kwargs) -> Dict[str, Any]:
        """创建仪表板统计数据。"""
        return {
            "total_users": kwargs.get("total_users", random.randint(1, 50)),
            "total_content": kwargs.get("total_content", random.randint(10, 500)),
            "total_plays": kwargs.get("total_plays", random.randint(100, 10000)),
            "total_duration_seconds": kwargs.get("total_duration_seconds", random.randint(36000, 3600000)),
            "active_users_today": kwargs.get("active_users_today", random.randint(1, 20)),
            "top_content": kwargs.get("top_content", []),
            "top_users": kwargs.get("top_users", []),
        }

    @classmethod
    def create_batch_daily_stats(cls, count: int = 7, **kwargs) -> list:
        """批量创建每日统计数据。

        Args:
            count: 创建数量
            **kwargs: 传递给create_daily_stats的参数

        Returns:
            list: 每日统计数据列表
        """
        stats_list = []
        for i in range(count):
            date = datetime.utcnow().date() - timedelta(days=i)
            stats = cls.create_daily_stats(date=date.isoformat(), **kwargs)
            stats_list.append(stats)
        return stats_list


def create_daily_stats(**kwargs) -> Dict[str, Any]:
    """便捷函数：创建每日统计。"""
    return StatsFactory.create_daily_stats(**kwargs)


def create_weekly_stats(**kwargs) -> Dict[str, Any]:
    """便捷函数：创建每周统计。"""
    return StatsFactory.create_weekly_stats(**kwargs)


def create_monthly_stats(**kwargs) -> Dict[str, Any]:
    """便捷函数：创建每月统计。"""
    return StatsFactory.create_monthly_stats(**kwargs)


def create_dashboard_stats(**kwargs) -> Dict[str, Any]:
    """便捷函数：创建仪表板统计。"""
    return StatsFactory.create_dashboard_stats(**kwargs)
