import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base

class TrophySeason(Base):
    __tablename__ = 'trophy_trophystaff'

    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    season_id = Column(ForeignKey("camps_season.id"), nullable=False, default=0, doc='Season')
    trophy_id = Column(ForeignKey("trophy_trophy.id"), nullable=False, default=0, doc='Trophy')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )