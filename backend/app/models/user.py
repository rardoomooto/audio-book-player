import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from backend.app.core.database import Base
from .base import TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=True)
    status = Column(String(20), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships (optional for now; useful when wiring ORM usage)
    # play_records = relationship("PlayRecord", back_populates="user")
