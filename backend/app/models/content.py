import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship

from backend.app.core.database import Base
from .base import TimeStampMixin


class Folder(Base, TimeStampMixin):
    __tablename__ = "folders"

    folder_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    path = Column(String(500), nullable=False)
    parent_id = Column(String(36), ForeignKey("folders.folder_id"), nullable=True)

    # Relationships
    parent = relationship("Folder", remote_side=[folder_id], backref="subfolders")


class Content(Base, TimeStampMixin):
    __tablename__ = "contents"

    content_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=True)
    album = Column(String(100), nullable=True)
    series = Column(String(100), nullable=True)
    path = Column(String(500), nullable=False)
    file_format = Column(String(20), nullable=False)
    duration_seconds = Column(Integer, nullable=True)
    cover_path = Column(String(500), nullable=True)
    content_metadata = Column(JSON, nullable=True)
    folder_id = Column(String(36), ForeignKey("folders.folder_id"), nullable=True)

    # Relationships
    folder = relationship("Folder", backref="contents")
