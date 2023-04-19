import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base

class CamperInCamp(Base):
    __tablename__ = 'camps_camperincamp'
    __table_args__ = (
        UniqueConstraint('camp_id', 'camper_id'),
    )

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    status = Column(ForeignKey("catalogs_constant.id"), nullable=False, default=0, doc='Status de inscripción')
    payment_balance = Column(Float(53), nullable=False)
    camp_id = Column(ForeignKey("camps_camp.id"), nullable=False, default=0, doc='Campamento')
    camper_id = Column(ForeignKey("campers_camper.id"), nullable=False, default=0, doc='Camper')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
