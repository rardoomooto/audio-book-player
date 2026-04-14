from typing import List, Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import csv
import io

from backend.app.core.database import get_db
from backend.app.services.stats import StatisticsService
from sqlalchemy.orm import Session

router = APIRouter()


class DailyStatResponse(BaseModel):
    date: str
    plays: int
    duration_seconds: int
    content_count: int = 0


class UserStatResponse(BaseModel):
    user_id: str
    plays: int
    duration_seconds: int
    content_count: int
    first_play: Optional[str] = None
    last_play: Optional[str] = None
    top_content: List[dict] = []


class ContentStatResponse(BaseModel):
    content_id: str
    plays: int
    duration_seconds: int
    user_count: int
    first_play: Optional[str] = None
    last_play: Optional[str] = None
    top_users: List[dict] = []


class DashboardStatResponse(BaseModel):
    total_users: int
    total_contents: int
    total_plays: int
    total_duration_seconds: int
    today_plays: int
    today_duration_seconds: int
    week_plays: int
    month_plays: int


class RecentActivityResponse(BaseModel):
    record_id: str
    user_id: str
    user_name: str
    content_id: str
    content_title: str
    start_time: Optional[str]
    duration_seconds: int
    action: str


def get_stats_service(db: Session = Depends(get_db)) -> StatisticsService:
    """获取统计服务实例。"""
    return StatisticsService(db)


@router.get("/daily", response_model=List[DailyStatResponse])
def daily_stats(
    user_id: Optional[str] = Query(None, description="User ID to filter by"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(30, ge=1, le=365, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    stats_service: StatisticsService = Depends(get_stats_service)
) -> List[DailyStatResponse]:
    """获取每日统计。
    
    返回指定日期范围内的每日播放统计。
    """
    stats = stats_service.get_daily_stats(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset
    )
    return [DailyStatResponse(**s) for s in stats]


@router.get("/weekly", response_model=List[DailyStatResponse])
def weekly_stats(
    user_id: Optional[str] = Query(None, description="User ID to filter by"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(52, ge=1, le=52, description="Number of weeks to return"),
    stats_service: StatisticsService = Depends(get_stats_service)
) -> List[DailyStatResponse]:
    """获取每周统计。
    
    返回指定日期范围内的每周播放统计聚合。
    """
    stats = stats_service.get_weekly_stats(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
    return [DailyStatResponse(**s) for s in stats]


@router.get("/monthly", response_model=List[DailyStatResponse])
def monthly_stats(
    user_id: Optional[str] = Query(None, description="User ID to filter by"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(24, ge=1, le=60, description="Number of months to return"),
    stats_service: StatisticsService = Depends(get_stats_service)
) -> List[DailyStatResponse]:
    """获取每月统计。
    
    返回指定日期范围内的每月播放统计聚合。
    """
    stats = stats_service.get_monthly_stats(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
    return [DailyStatResponse(**s) for s in stats]


@router.get("/yearly", response_model=List[DailyStatResponse])
def yearly_stats(
    user_id: Optional[str] = Query(None, description="User ID to filter by"),
    limit: int = Query(10, ge=1, le=20, description="Number of years to return"),
    stats_service: StatisticsService = Depends(get_stats_service)
) -> List[DailyStatResponse]:
    """获取每年统计。
    
    返回指定年份范围内的每年播放统计聚合。
    """
    stats = stats_service.get_yearly_stats(
        user_id=user_id,
        limit=limit
    )
    return [DailyStatResponse(**s) for s in stats]


@router.get("/dashboard", response_model=DashboardStatResponse)
def dashboard_stats(
    stats_service: StatisticsService = Depends(get_stats_service)
) -> DashboardStatResponse:
    """获取仪表板统计。
    
    返回系统总览统计信息，包括用户数、内容数、播放次数等。
    """
    stats = stats_service.get_dashboard_stats()
    return DashboardStatResponse(**stats)


@router.get("/users/{user_id}", response_model=UserStatResponse)
def user_stats(
    user_id: str,
    stats_service: StatisticsService = Depends(get_stats_service)
) -> UserStatResponse:
    """获取用户统计。
    
    返回指定用户的播放统计信息，包括总播放次数、总时长、最常播放的内容等。
    """
    stats = stats_service.get_user_stats(user_id)
    return UserStatResponse(**stats)


@router.get("/contents/{content_id}", response_model=ContentStatResponse)
def content_stats(
    content_id: str,
    stats_service: StatisticsService = Depends(get_stats_service)
) -> ContentStatResponse:
    """获取内容统计。
    
    返回指定内容的播放统计信息，包括播放次数、播放用户数、最常播放的用户等。
    """
    stats = stats_service.get_content_stats(content_id)
    return ContentStatResponse(**stats)


@router.get("/activity/recent", response_model=List[RecentActivityResponse])
def recent_activity(
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    stats_service: StatisticsService = Depends(get_stats_service)
) -> List[RecentActivityResponse]:
    """获取最近活动。
    
    返回最近的播放活动记录。
    """
    activities = stats_service.get_recent_activity(limit=limit)
    return [RecentActivityResponse(**a) for a in activities]


@router.get("/export/daily")
def export_daily_stats(
    user_id: Optional[str] = Query(None, description="User ID to filter by"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    stats_service: StatisticsService = Depends(get_stats_service)
) -> StreamingResponse:
    """导出每日统计为CSV。
    
    返回CSV格式的每日播放统计数据。
    """
    stats = stats_service.get_daily_stats(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        limit=365,
        offset=0
    )
    
    # 创建CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入表头
    writer.writerow(['Date', 'Plays', 'Duration (seconds)', 'Content Count'])
    
    # 写入数据
    for s in stats:
        writer.writerow([
            s['date'],
            s['plays'],
            s['duration_seconds'],
            s.get('content_count', 0)
        ])
    
    # 设置响应头
    output.seek(0)
    filename = f"daily_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/export/users/{user_id}")
def export_user_stats(
    user_id: str,
    stats_service: StatisticsService = Depends(get_stats_service)
) -> StreamingResponse:
    """导出用户统计为CSV。
    
    返回CSV格式的用户播放统计数据。
    """
    stats = stats_service.get_user_stats(user_id)
    
    # 创建CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入表头
    writer.writerow(['User ID', 'Total Plays', 'Duration (seconds)', 'Content Count', 'First Play', 'Last Play'])
    
    # 写入数据
    writer.writerow([
        stats['user_id'],
        stats['plays'],
        stats['duration_seconds'],
        stats['content_count'],
        stats.get('first_play', ''),
        stats.get('last_play', '')
    ])
    
    # 写入最常播放的内容（如果存在）
    if stats.get('top_content'):
        writer.writerow([])
        writer.writerow(['Top Content'])
        writer.writerow(['Content ID', 'Play Count', 'Total Duration'])
        for tc in stats['top_content']:
            writer.writerow([
                tc['content_id'],
                tc['play_count'],
                tc['total_duration']
            ])
    
    output.seek(0)
    filename = f"user_{user_id}_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/export/contents/{content_id}")
def export_content_stats(
    content_id: str,
    stats_service: StatisticsService = Depends(get_stats_service)
) -> StreamingResponse:
    """导出内容统计为CSV。
    
    返回CSV格式的内容播放统计数据。
    """
    stats = stats_service.get_content_stats(content_id)
    
    # 创建CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入表头
    writer.writerow(['Content ID', 'Total Plays', 'Duration (seconds)', 'User Count', 'First Play', 'Last Play'])
    
    # 写入数据
    writer.writerow([
        stats['content_id'],
        stats['plays'],
        stats['duration_seconds'],
        stats['user_count'],
        stats.get('first_play', ''),
        stats.get('last_play', '')
    ])
    
    # 写入最常播放的用户（如果存在）
    if stats.get('top_users'):
        writer.writerow([])
        writer.writerow(['Top Users'])
        writer.writerow(['User ID', 'Play Count', 'Total Duration'])
        for tu in stats['top_users']:
            writer.writerow([
                tu['user_id'],
                tu['play_count'],
                tu['total_duration']
            ])
    
    output.seek(0)
    filename = f"content_{content_id}_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
