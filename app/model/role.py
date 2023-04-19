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
