import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base

class TrophyStaff(Base):
    __tablename__ = 'trophy_trophystaff_holder'
    __table_args__ = (
        UniqueConstraint('trophystaff_id', 'staff_id'),
    )

    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    trophy_season_id = Column("trophystaff_id", ForeignKey("trophy_trophystaff.id"), nullable=False, default=0, doc='Status de inscripción')
    staff_id = Column(ForeignKey("staff_staff.id"), nullable=False, default=0, doc='Status de inscripción')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
