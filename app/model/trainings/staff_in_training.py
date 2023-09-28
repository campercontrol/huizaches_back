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
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base


class StaffInTraining(Base):
    __tablename__ = "camps_staffintraining"
    __table_args__ = (
        UniqueConstraint('training_event_id', 'staff_id'),
    )

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    assist = Column(Boolean, nullable=False)
    confirmed_staff = Column(Boolean, nullable=False)
    staff_id = Column(
        ForeignKey("staff_staff.id"), nullable=False, default=0, doc="Staff"
    )
    training_event_id = Column(
        ForeignKey("camps_trainingevent.id"),
        nullable=False,
        default=0,
        doc="Evento de capacitación ",
    )
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
