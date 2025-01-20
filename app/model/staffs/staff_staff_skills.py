from sqlalchemy import Column,  Integer, ForeignKey, UniqueConstraint
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, 
from utils.db import Base
class StaffSkills(Base):
    __tablename__ = 'staff_staff_skills'
    __table_args__ = (
        UniqueConstraint('staff_id', 'skill_id'),
    )
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    staff_id = Column('staff_id', ForeignKey('staff_staff.id', ondelete="cascade"), nullable=False)
    skill_id = Column("skill_id", ForeignKey('staff_skill.id', ondelete="cascade"), nullable=False)
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )