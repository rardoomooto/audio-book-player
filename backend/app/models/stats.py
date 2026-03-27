import uuid
from datetime import date
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.core.database import Base
from .base import TimeStampMixin


class DailyStats(Base, TimeStampMixin):
    __tablename__ = "daily_stats"

    statistics_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    date = Column(Date, nullable=False)
    total_duration_seconds = Column(Integer, nullable=False, default=0)
    content_count = Column(Integer, nullable=False, default=0)
    most_played_content_id = Column(String(36), ForeignKey("contents.content_id"), nullable=True)

    user = relationship("User", backref="daily_stats")
    most_played_content = relationship("Content", uselist=False)
