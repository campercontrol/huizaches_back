import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class PaymentsAccounts(Base):
    __tablename__ = "payments_accounts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name_payments_accounts = Column(String(150), default='')
    bank = Column(String(30), default='')
    account_number = Column(Integer(10), positive=True, default='')
    clabe_number = Column(Integer(10), positive=True, default='')
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
