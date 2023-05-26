import uuid
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Integer
from utils.db import Base

class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    url = Column(String(200), nullable=False)
    icon = Column(String(200), nullable=False)
    language = Column(String(2), nullable=False)
    is_coordinator = Column(Boolean, nullable=False,index = True) 
    is_admin = Column(Boolean, nullable=False, index = True)
    is_employee = Column(Boolean, nullable=False, index = True)
    target = Column(Boolean, nullable=False)
    order = Column(Integer, nullable=False)
    new_window = Column(Boolean, index = True)
    role_id = Column(
        Integer,
        ForeignKey("role.id"),
        index=True,
    )
    is_active = Column(Boolean, nullable=False, index = True, default = True)
    created_at = Column(
        DateTime(timezone=True), 
        default=datetime.utcnow
        )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    