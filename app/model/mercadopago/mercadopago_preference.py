from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer
)
from utils.db import Base
class MercadopagoPreference(Base):
    __tablename__ = "mercadopago_preference"
    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    camp_id = Column(
        ForeignKey("camps_camp.id", ondelete="cascade"), nullable=False, doc="Campamento"
    )
    camper_id = Column(
        ForeignKey("campers_camper.id", ondelete="cascade"), nullable=False, doc='Camper'
    )
    preference_id = Column(Integer, nullable=False, unique=True)
    external_id = Column(Integer, nullable=False, unique=True)
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
