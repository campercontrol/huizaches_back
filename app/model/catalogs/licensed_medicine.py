import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class LicensedMedicine (Base):
    __tablename__ = "licensed_medicine"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name_licensed_medicine = Column(String(150), default='')
    assigned = Column(SmallInteger(), default='0')
    order = Column(Integer(), positive=True, default='1')
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
