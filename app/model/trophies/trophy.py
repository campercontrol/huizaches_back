import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base

class Trophy(Base):
    __tablename__ = 'trophy_trophy'

    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    name = Column(String(150), nullable=False)
    description = Column(String(150), nullable=False)
    photo = Column(String(512))
    active = Column(Boolean, nullable=False)
    trophy_type = Column(ForeignKey("catalogs_constant.id"), nullable=False, default=0, doc='Tipo de trofeo')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
