from enum import Enum
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ...services.playback import get_playback_service, PlaybackState
from ...api.deps import get_current_user

router = APIRouter()


class PlaybackRequest(BaseModel):
    content_id: str
    position_seconds: int = Field(0, ge=0, description="起始位置（秒）")


class PositionUpdate(BaseModel):
    position_seconds: int = Field(..., ge=0, description="播放位置（秒）")


class PlayLimitUpdate(BaseModel):
    daily_minutes: int = Field(..., ge=0, description="每日限制分钟数")
    weekly_minutes: Optional[int] = Field(None, ge=0, description="每周限制分钟数")
    monthly_minutes: Optional[int] = Field(None, ge=0, description="每月限制分钟数")
    yearly_minutes: Optional[int] = Field(None, ge=0, description="每年限制分钟数")


@router.post("/play")
def play(req: PlaybackRequest, current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
    """开始播放。"""
    try:
        service = get_playback_service()
        result = service.start_playback(
            user_id=current_user["username"],
            content_id=req.content_id,
            position_seconds=req.position_seconds,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/pause")
def pause(req: PlaybackRequest, current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
    """暂停播放。"""
    try:
        service = get_playback_service()
        result = service.pause_playback(
            user_id=current_user["username"],
            content_id=req.content_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/resume")
def resume(req: PlaybackRequest, current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
    """恢复播放。"""
    try:
        service = get_playback_service()
        result = service.resume_playback(
            user_id=current_user["username"],
            content_id=req.content_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/stop")
def stop(req: PlaybackRequest, current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
    """停止播放。"""
    try:
        service = get_playback_service()
        result = service.stop_playback(
            user_id=current_user["username"],
            content_id=req.content_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/position")
def update_position(pos: PositionUpdate, current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
    """更新播放位置。"""
    try:
        service = get_playback_service()
        # 获取当前播放会话
        current = service.get_current_playback(current_user["username"])
        if not current:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="没有正在进行的播放会话")
        
        result = service.update_position(
            user_id=current_user["username"],
            content_id=current["content_id"],
            position_seconds=pos.position_seconds,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/current")
def current(current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
    """获取当前播放状态。"""
    service = get_playback_service()
    result = service.get_current_playback(current_user["username"])
    if result:
        return result
    return {"state": PlaybackState.IDLE.value, "content_id": None, "user_id": None}


@router.get("/session/{session_id}")
def get_session(session_id: str, current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
    """获取播放会话信息。"""
    service = get_playback_service()
    result = service.get_playback_session(session_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="播放会话不存在")
    
    # 检查权限
    if result["user_id"] != current_user["username"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权访问此播放会话")
    
    return result


@router.get("/limits")
def get_play_limits(current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
    """获取用户播放限制。"""
    service = get_playback_service()
    return service.get_play_limit(current_user["username"])


@router.put("/limits")
def update_play_limits(limits: PlayLimitUpdate, current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
    """更新用户播放限制（仅管理员）。"""
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="需要管理员权限")
    
    service = get_playback_service()
    service.set_play_limit(
        user_id=current_user["username"],
        daily_minutes=limits.daily_minutes,
        weekly_minutes=limits.weekly_minutes,
        monthly_minutes=limits.monthly_minutes,
        yearly_minutes=limits.yearly_minutes,
    )
    
    return {"detail": "播放限制已更新"}


@router.get("/today-time")
def get_today_play_time(current_user: Dict = Depends(get_current_user)) -> Dict[str, Any]:
    """获取用户今日播放时长。"""
    service = get_playback_service()
    minutes = service.get_today_play_time(current_user["username"])
    return {"today_minutes": minutes}
