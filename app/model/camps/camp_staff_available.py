from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from utils.db import Base
from sqlalchemy.schema import UniqueConstraint

class CampStaffAvailable(Base):
    __tablename__ = 'camps_camp_staff_available'
    __table_args__ = (
        UniqueConstraint('camp_id', 'staff_id'),
    )
    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    camp_id = Column(ForeignKey("camps_camp.id"), nullable=False, doc='Campamento')
    staff_id = Column(ForeignKey("staff_staff.id"), nullable=False, doc="Staff")