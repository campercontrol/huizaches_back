import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base

class CampPaymentAccount(Base):
    __tablename__ = 'camps_camp_payments_accounts'
    __table_args__ = (
        UniqueConstraint('camp_id', 'paymentaccounts_id'),
    )
    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    camp_id = Column("camp_id", Integer, nullable=False, index=True)
    paymentaccount_id = Column("paymentaccounts_id", Integer, nullable=False, index=True)