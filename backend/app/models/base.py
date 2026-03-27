from backend.app.core.database import Base

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TimeStampMixin:
    """Mixin to provide created_at / updated_at timestamps for all models."""

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


__all__ = ["Base", "TimeStampMixin"]
