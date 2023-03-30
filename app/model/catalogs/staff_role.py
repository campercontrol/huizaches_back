import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class StaffRole(Base):
    __tablename__ = "catalogs_staff_role"
    #catalogs_staffroles en cc2

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    name = Column("name",String(150), default='', nullable=False, doc='Nombre del Rol')
    payment = Column("payment",Float(precision=2), default='0', doc='Pago por día')
    color = Column("color",String(15), default='', nullable=False, doc='Color de rol')
    created_at = Column("created",DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
