import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base

class StaffInCamp(Base):
    __tablename__ = 'camps_staffincamp'

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    confirmed_staff = Column(Boolean, nullable=False)
    assigned_role_id = Column(ForeignKey("catalogs_staff_role.id"), doc='Rol de staff')
    camp_id = Column(ForeignKey("camps_camp.id"), nullable=False, default=0, doc='Campamento')
    staff_id = Column(ForeignKey("staff_staff.id"), nullable=False, default=0, doc='Staff')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
