import uuid
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from utils.db import Base


class Role(Base):
    __tablename__ = "role"
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
        doc="id del rol",
        index=True
    )
    name = Column(String(30))
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"{self.id} - {self.name} - {self.is_active} - {self.created_at} - {self.updated_at}"


