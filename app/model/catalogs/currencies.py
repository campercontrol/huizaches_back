import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class Currencies(Base):
    __tablename__="currencies"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name_currency = Column(String(150), default='', nullable=False, doc='Nombre de la divisa')
    symbol = Column(String(10), default='', nullable=False, doc='Simbolo de la divisa')
    acronyms = Column(String(10), default='', nullable=False, doc='Siglas')
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
