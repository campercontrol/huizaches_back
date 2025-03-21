from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from utils.db import Base

class StaffSendercamp(Base):
    __tablename__ = 'camps_staffsendercamp'
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    camp_id = Column(ForeignKey("camps_camp.id"), nullable=False, doc='Campamento')
    staff_id = Column(ForeignKey("staff_staff.id"), nullable=False, doc='Staff')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
