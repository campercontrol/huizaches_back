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
class Grouping(Base):
    __tablename__ = 'grouping_grouping'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id")
    name = Column(String(512), nullable=False)
    is_active = Column(Boolean, nullable=False)
    grouping_type_id = Column(
        Integer,
        ForeignKey("grouping_groupingtype.id"),
        index=True,
    )
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


