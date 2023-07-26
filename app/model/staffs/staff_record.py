import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class StaffRecord(Base):
    __tablename__ = 'staff_userrecords'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id del camper_checkpoint")
    attend = Column(Integer, nullable=False)
    attended = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
