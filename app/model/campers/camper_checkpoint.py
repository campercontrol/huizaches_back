import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class CamperCheckpoint(Base):
    __tablename__ = 'camps_checkpointcamper'
    __table_args__ = (
        UniqueConstraint('checkpoint_id', 'camper_id'),
    )

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id del camper_checkpoint")
    checkin = Column(Boolean, nullable=False)
    checkin_date = Column(DateTime(True), nullable=False)
    camper_id = Column(ForeignKey("campers_camper.id"), nullable=False, default=0, doc='Camper')
    checkpoint_id = Column(ForeignKey("camps_checkpoint.id"), nullable=False, default=0, doc='Checkpoint')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
