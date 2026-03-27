import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.core.database import Base
from .base import TimeStampMixin


class UserPermission(Base, TimeStampMixin):
    __tablename__ = "user_permissions"

    permission_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    folder_id = Column(String(36), ForeignKey("folders.folder_id"), nullable=False)
    permission_type = Column(String(20), nullable=False)

    # Relationships (optional)
    user = relationship("User", backref="permissions")
    folder = relationship("Folder", backref="permissions")
