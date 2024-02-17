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
    Date,
    Time,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class MedicalStaffVisit(Base):
    __tablename__ = "medical_staffmedicalvisit"

    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    medical_tracing = Column(Boolean, nullable=False)
    doctor = Column(String(60), nullable=False)
    attention_date = Column(Date, nullable=False)
    attention_time = Column(Time, nullable=False)
    diagnostic = Column(String(60), nullable=False)
    description = Column(Text)
    triage = Column(
        ForeignKey("catalogs_constant.id"), nullable=False, default=0, doc="Camper"
    )
    camp_restriction = Column(Text)
    administered_medications = Column(Text)
    medical_monitoring = Column(Text)
    comment = Column(Text)
    camp_id = Column(
        "camp", ForeignKey("camps_camp.id"), nullable=True, doc="Campamento"
    )
    initial_visit_id = Column(
        "medical_camper_visit",
        ForeignKey("medical_campermedicalvisit.id"),
        nullable=True,
        doc="Medical Camper Visit",
    )
    staff_id = Column(
        ForeignKey("staff_staff.id"), nullable=False, default=0, doc="Staff"
    )
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
