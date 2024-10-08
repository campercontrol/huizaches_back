from datetime import datetime
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Boolean
)
from utils.db import Base
class MercadopagoMerchantOrder(Base):
    __tablename__ = "mercadopago_merchant_order"
    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    camp_id = Column(
        ForeignKey("camps_camp.id", ondelete="cascade"), nullable=False, doc="Campamento"
    )
    camper_id = Column(
        ForeignKey("campers_camper.id", ondelete="cascade"), nullable=False, doc='Camper'
    )
    status = Column(Boolean, nullable=False)
    external_id = Column(
        ForeignKey("mercadopago_preference.external_id", ondelete="cascade"), nullable=False
    )
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
