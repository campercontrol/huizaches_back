import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Float,
    Date
)
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base
class PaymentTransactionType(Base):
    __tablename__ = 'payments_paymenttransactiontype'

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id del tipo de transacción")
    name = Column(String(100), nullable=False)
    movement = Column(Integer, nullable=False)
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )