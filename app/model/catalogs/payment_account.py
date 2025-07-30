import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class PaymentAccount(Base):
    __tablename__ = "catalogs_payment_account"
    #catalogs_paymentaccounts

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    name = Column("name", String(150), nullable=False, default='')
    bank = Column("bank", String(30), nullable=False, default='')
    account_number = Column("account_number", String(12), nullable=False)
    clabe_number = Column("clabe_number", String(18), nullable=False)
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"{self.id} - {self.name} - {self.bank} - {self.account_number} - {self.created_at} - {self.updated_at}"
