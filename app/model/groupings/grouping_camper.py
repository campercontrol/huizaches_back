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
    Date
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class GroupingCamper(Base):
    __tablename__ = 'grouping_groupingcamper'
    __table_args__ = (
        UniqueConstraint('grouping_camp_id', 'camper_id'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id")
    camper_id = Column(
        Integer,
        ForeignKey("campers_camper.id"),
        index=True,
    )
    grouping_camp_id = Column(
        Integer,
        ForeignKey("grouping_groupingcamp.id"),
        index=True,
    )
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

