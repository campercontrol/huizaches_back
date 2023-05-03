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
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base


class CamperExtraCharge(Base):
    __tablename__ = "payments_camperextracharge"
    __table_args__ = (UniqueConstraint("extra_charge_id", "camper_id"),)

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    is_selected = Column(Boolean, nullable=False)
    created = Column(DateTime(True), nullable=False)
    updated = Column(DateTime(True), nullable=False)
    camper_id = Column(
        ForeignKey("campers_camper.id"), 
        nullable=False, 
        default=0, 
        doc="Camper"
    )
    extra_charge_id = Column(
        ForeignKey("camps_campextracharge.id"),
        nullable=False,
        default=0,
        doc="Camp Extra Charge",
    )
