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
class GroupingCamp(Base):
    __tablename__ = 'grouping_groupingcamp'
    __table_args__ = (
        UniqueConstraint('camp_id', 'grouping_id'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id")
    maximum_capacity = Column(Integer, nullable=False)
    camp_id = Column(
        Integer,
        ForeignKey("camps_camp.id"),
        index=True,
    )
    grouping_id = Column(
        Integer,
        ForeignKey("grouping_grouping.id"),
        index=True,
    )
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
