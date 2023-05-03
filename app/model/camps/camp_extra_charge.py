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
)
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base


class CampExtraCharge(Base):
    __tablename__ = "camps_campextracharge"

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(250), nullable=False)
    price = Column(Float(53), nullable=False)
    currency_id = Column(
        ForeignKey("catalogs_currency.id"), nullable=False, default=0, doc="Divisa"
    )
    camp_id = Column(
        ForeignKey("camps_camp.id"), nullable=False, default=0, doc="Campamento"
    )
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
