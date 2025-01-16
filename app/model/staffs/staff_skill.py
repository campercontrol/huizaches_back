from sqlalchemy import Column,  Integer, String
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from utils.db import Base
class StaffSkill(Base):
    __tablename__ = 'staff_skill'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="Id del staff_skill")
    name = Column(String(150))
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )