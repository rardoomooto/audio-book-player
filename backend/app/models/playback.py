import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.core.database import Base
from .base import TimeStampMixin


class PlayLimit(Base, TimeStampMixin):
    __tablename__ = "play_limits"

    limit_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=True)
    daily_minutes = Column(Integer, nullable=False, default=0)
    weekly_minutes = Column(Integer, nullable=True)
    monthly_minutes = Column(Integer, nullable=True)
    yearly_minutes = Column(Integer, nullable=True)

    user = relationship("User", backref="play_limits")


class PlayRecord(Base, TimeStampMixin):
    __tablename__ = "play_records"

    record_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    content_id = Column(String(36), ForeignKey("contents.content_id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    play_position_seconds = Column(Integer, nullable=True)

    user = relationship("User", backref="play_records")
    content = relationship("Content", backref="play_records")
