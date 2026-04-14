"""测试数据工厂 - Limits模型。"""

from datetime import datetime
from typing import Dict, Any, Optional


class LimitsFactory:
    """时长限制工厂类。"""

    _next_id = 1

    @classmethod
    def create_play_limit(cls, **kwargs) -> Dict[str, Any]:
        """创建播放限制。

        Args:
            user_id: 用户ID（None表示全局限制）
            daily_minutes: 每日限制分钟数
            weekly_minutes: 每周限制分钟数
            monthly_minutes: 每月限制分钟数
            yearly_minutes: 每年限制分钟数

        Returns:
            Dict[str, Any]: 播放限制数据
        """
        limit_id = kwargs.get("id", cls._next_id)
        cls._next_id += 1

        return {
            "id": limit_id,
            "user_id": kwargs.get("user_id"),  # None = global
            "daily_minutes": kwargs.get("daily_minutes", 60),
            "weekly_minutes": kwargs.get("weekly_minutes", 420),
            "monthly_minutes": kwargs.get("monthly_minutes", 1800),
            "yearly_minutes": kwargs.get("yearly_minutes", 21900),
            "created_at": kwargs.get("created_at", datetime.utcnow().isoformat()),
            "updated_at": kwargs.get("updated_at", datetime.utcnow().isoformat()),
        }

    @classmethod
    def create_global_limit(cls, **kwargs) -> Dict[str, Any]:
        """创建全局播放限制。

        Args:
            daily_minutes: 每日限制分钟数
            weekly_minutes: 每周限制分钟数
            monthly_minutes: 每月限制分钟数
            yearly_minutes: 每年限制分钟数

        Returns:
            Dict[str, Any]: 全局限制数据
        """
        return cls.create_play_limit(
            user_id=None,
            **kwargs
        )

    @classmethod
    def create_user_limit(cls, user_id: int, **kwargs) -> Dict[str, Any]:
        """创建用户特定限制。

        Args:
            user_id: 用户ID
            daily_minutes: 每日限制分钟数
            weekly_minutes: 每周限制分钟数
            monthly_minutes: 每月限制分钟数
            yearly_minutes: 每年限制分钟数

        Returns:
            Dict[str, Any]: 用户限制数据
        """
        return cls.create_play_limit(
            user_id=user_id,
            **kwargs
        )

    @classmethod
    def create_unlimited_limit(cls, user_id: Optional[int] = None) -> Dict[str, Any]:
        """创建无限制配置。

        Args:
            user_id: 用户ID（None表示全局）

        Returns:
            Dict[str, Any]: 无限制配置
        """
        return cls.create_play_limit(
            user_id=user_id,
            daily_minutes=0,  # 0 = no limit
            weekly_minutes=0,
            monthly_minutes=0,
            yearly_minutes=0,
        )

    @classmethod
    def create_strict_limit(cls, user_id: Optional[int] = None) -> Dict[str, Any]:
        """创建严格限制配置。

        Args:
            user_id: 用户ID（None表示全局）

        Returns:
            Dict[str, Any]: 严格限制配置
        """
        return cls.create_play_limit(
            user_id=user_id,
            daily_minutes=30,
            weekly_minutes=180,
            monthly_minutes=720,
            yearly_minutes=8640,
        )

    @classmethod
    def create_relaxed_limit(cls, user_id: Optional[int] = None) -> Dict[str, Any]:
        """创建宽松限制配置。

        Args:
            user_id: 用户ID（None表示全局）

        Returns:
            Dict[str, Any]: 宽松限制配置
        """
        return cls.create_play_limit(
            user_id=user_id,
            daily_minutes=240,  # 4 hours
            weekly_minutes=1680,  # 28 hours
            monthly_minutes=7200,  # 120 hours
            yearly_minutes=87600,  # 1460 hours
        )


def create_play_limit(**kwargs) -> Dict[str, Any]:
    """便捷函数：创建播放限制。"""
    return LimitsFactory.create_play_limit(**kwargs)


def create_global_limit(**kwargs) -> Dict[str, Any]:
    """便捷函数：创建全局限制。"""
    return LimitsFactory.create_global_limit(**kwargs)


def create_user_limit(user_id: int, **kwargs) -> Dict[str, Any]:
    """便捷函数：创建用户限制。"""
    return LimitsFactory.create_user_limit(user_id, **kwargs)
