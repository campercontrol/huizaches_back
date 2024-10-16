from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    BigInteger
)
from utils.db import Base
class MercadopagoPayment(Base):
    __tablename__ = "mercadopago_payment"
    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    camp_id = Column(
        ForeignKey("camps_camp.id", ondelete="cascade"), nullable=False, doc="Campamento"
    )
    camper_id = Column(
        ForeignKey("campers_camper.id", ondelete="cascade"), nullable=False, doc='Camper'
    )
    payment_id = Column(BigInteger, nullable=False, unique=True)
    status = Column(String, nullable=False)
    external_id = Column(
        ForeignKey("mercadopago_preference.external_id", ondelete="cascade"), nullable=False
    )
    internal_payment_id = Column(
        ForeignKey("payments_payment.id", ondelete="cascade")
    )
    
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
