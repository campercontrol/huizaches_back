import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class StaffRoles(Base):
    __tablename__ = "staff_roles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name_staff_roles = Column(String(150), default='', nullable=False, doc='Nombre del Rol')
    payment = Column(Float(precision=2), default='0', doc='Pago por día')
    color = Column(String(15), default='', nullable=False, doc='Color de rol')
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
