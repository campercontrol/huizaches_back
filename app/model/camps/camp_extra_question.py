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


class CampExtraQuestion(Base):
    __tablename__ = "camps_extraquestion"

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    question = Column(Text, nullable=False)
    is_required = Column(Boolean, nullable=False)
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
