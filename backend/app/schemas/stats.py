from datetime import date, datetime
from typing import List
from pydantic import BaseModel


class DailyStat(BaseModel):
    date: date
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


class DashboardStat(BaseModel):
    total_users: int
    total_contents: int
    total_plays: int
