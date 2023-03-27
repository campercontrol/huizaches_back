import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class Vaccines(Base):
    __tablename__ = "vaccines"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name_vaccines = Column(String(), default='', anullable=False, docs='Nombre de vacuna')
    assigned = Column(SmallInteger(), default='0')
    order = Column(Integer(), positive=True, default='1')
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
