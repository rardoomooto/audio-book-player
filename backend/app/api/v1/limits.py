from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ...services.playback import get_playback_service
from ...api.deps import get_current_user, get_current_admin_user

router = APIRouter()


class GlobalLimitUpdate(BaseModel):
    daily_minutes: int = Field(..., ge=0, description="每日限制分钟数")
    weekly_minutes: Optional[int] = Field(None, ge=0, description="每周限制分钟数")
    monthly_minutes: Optional[int] = Field(None, ge=0, description="每月限制分钟数")
    yearly_minutes: Optional[int] = Field(None, ge=0, description="每年限制分钟数")


class UserLimitUpdate(BaseModel):
    daily_minutes: int = Field(..., ge=0, description="每日限制分钟数")
    weekly_minutes: Optional[int] = Field(None, ge=0, description="每周限制分钟数")
    monthly_minutes: Optional[int] = Field(None, ge=0, description="每月限制分钟数")
    yearly_minutes: Optional[int] = Field(None, ge=0, description="每年限制分钟数")


@router.get("/global")
def get_global_limit(current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
    """获取全局播放限制。"""
    service = get_playback_service()
    return service.get_play_limit(None)


@router.put("/global")
def update_global_limit(
    limits: GlobalLimitUpdate,
    current_admin: Dict = Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """更新全局播放限制（仅管理员）。"""
    service = get_playback_service()
    service.set_play_limit(
        user_id=None,
        daily_minutes=limits.daily_minutes,
        weekly_minutes=limits.weekly_minutes,
        monthly_minutes=limits.monthly_minutes,
        yearly_minutes=limits.yearly_minutes,
    )
    return {"detail": "全局播放限制已更新"}


@router.get("/users/{user_id}")
def get_user_limit(
    user_id: str,
    current_user: Dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """获取用户播放限制。"""
    # 检查权限：管理员可以查看任何用户，普通用户只能查看自己
    if not current_user.get("is_admin", False) and current_user["username"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权查看此用户的限制")
    
    service = get_playback_service()
    return service.get_play_limit(user_id)


@router.put("/users/{user_id}")
def update_user_limit(
    user_id: str,
    limits: UserLimitUpdate,
    current_admin: Dict = Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """更新用户播放限制（仅管理员）。"""
    service = get_playback_service()
    service.set_play_limit(
        user_id=user_id,
        daily_minutes=limits.daily_minutes,
        weekly_minutes=limits.weekly_minutes,
        monthly_minutes=limits.monthly_minutes,
        yearly_minutes=limits.yearly_minutes,
    )
    return {"detail": f"用户 {user_id} 的播放限制已更新"}


@router.delete("/users/{user_id}")
def delete_user_limit(
    user_id: str,
    current_admin: Dict = Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """删除用户播放限制（恢复为全局限制）。"""
    # 这里我们只是设置一个默认值，而不是真正删除
    # 实际实现中可能需要更复杂的逻辑
    service = get_playback_service()
    service.set_play_limit(
        user_id=user_id,
        daily_minutes=0,  # 0表示使用全局限制
    )
    return {"detail": f"用户 {user_id} 的播放限制已重置为全局默认"}
