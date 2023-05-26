import uuid
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from utils.db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True,index=True,)
    email = Column(String(80),unique = True)
    hashed_pass = Column(String(200))
    role_id = Column(
        Integer,
        ForeignKey("role.id"),
        index=True,
    )

    is_coordinator = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=True)
    is_employee = Column(Boolean, default=True)

    is_superuser = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
