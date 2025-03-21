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
    Date,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class Payment(Base):
    __tablename__ = "payments_payment"

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    paid = Column(Boolean, nullable=False)
    payment_date = Column(Date)
    payment_amount = Column(Float(53), nullable=False)
    txn_number = Column(String(200), nullable=False)
    camp_id = Column(
        "camp", 
        ForeignKey("camps_camp.id", ondelete="cascade"), 
        nullable=True, 
        doc="Campamento"
    )
    camper_id = Column(
        "camper",
        ForeignKey("campers_camper.id", ondelete="cascade"),
        nullable=True,
        doc="Camper",
    )
    currency_id = Column(
        "currency",
        ForeignKey("catalogs_currency.id"),
        nullable=True,
        doc="Divisa",
    )
    parent_id = Column(
        "parent",
        ForeignKey("campers_parent.id", ondelete="cascade"),
        nullable=True,
        doc="Titular de la cuenta",
    )
    payment_method_id = Column(
        "payment_method",
        ForeignKey("payments_paymentmethod.id"),
        nullable=True,
        doc="Metodo de pago",
    )
    txn_type_id = Column(
        "txn_type",
        ForeignKey("payments_paymenttransactiontype.id"),
        nullable=True,
        doc="Metodo de pago",
    )
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
