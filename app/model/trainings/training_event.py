import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID


from utils.db import Base

class TrainingEvent(Base):
    __tablename__ = 'camps_trainingevent'

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    start = Column(DateTime(True), nullable=False)
    end = Column(DateTime(True), nullable=False)
    location = Column(String(120), nullable=False)
    open_enrollment = Column(Boolean, nullable=False)
    active = Column(Boolean, nullable=False)
    season_id = Column(ForeignKey("camps_season.id"), nullable=False, default=0, doc='Temporada')
    training_id = Column(ForeignKey("camps_training.id"), nullable=False, default=0, doc='Capacitacion')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
