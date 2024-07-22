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


class CamperExtraAnswer(Base):
    __tablename__ = "campers_extraanswers"

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    answer = Column(Text)
    camper_id = Column(
        ForeignKey("campers_camper.id", ondelete="cascade"), nullable=False, default=0, doc="Camper"
    )
    question_id = Column(
        ForeignKey("camps_extraquestion.id"),
        nullable=False,
        default=0,
        doc="Extra Question",
    )
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
