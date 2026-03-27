from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class DailyStat(BaseModel):
    date: str
    plays: int
    duration_seconds: int


class UserStat(BaseModel):
    user_id: int
    plays: int
    duration_seconds: int


class ContentStat(BaseModel):
    content_id: int
    plays: int
    duration_seconds: int


@router.get("/daily")
def daily_stats() -> List[DailyStat]:
    return [DailyStat(date="2026-03-01", plays=5, duration_seconds=300)]


@router.get("/weekly")
def weekly_stats() -> List[DailyStat]:
    return [DailyStat(date="2026-W10", plays=35, duration_seconds=2100)]


@router.get("/monthly")
def monthly_stats() -> List[DailyStat]:
    return [DailyStat(date="2026-03", plays=120, duration_seconds=7200)]


@router.get("/yearly")
def yearly_stats() -> List[DailyStat]:
    return [DailyStat(date="2026", plays=1400, duration_seconds=86400)]


@router.get("/dashboard")
def dashboard_stats() -> dict:
    return {"users": 2, "contents": 1, "plays": 5}


@router.get("/users/{user_id}")
def user_stats(user_id: int) -> UserStat:
    return UserStat(user_id=user_id, plays=10, duration_seconds=600)


@router.get("/contents/{content_id}")
def content_stats(content_id: int) -> ContentStat:
    return ContentStat(content_id=content_id, plays=3, duration_seconds=180)
