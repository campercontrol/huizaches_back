import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Date, ForeignKey, Integer, String, SmallInteger, Float, Text, Date, Table, Time
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID

from model.catalogs.constant import Constant

from utils.db import Base
class MedicalCamperVisit(Base):
    __tablename__ = 'medical_campermedicalvisit'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc='id de la consulta medica del camper')
    medical_tracing = Column(Boolean, nullable=False)
    doctor = Column(String(60), nullable=False)
    attention_date = Column(Date, nullable=False)
    attention_time = Column(Time, nullable=False)
    diagnostic = Column(String(60), nullable=False)
    description = Column(Text)
    triage = Column(
        ForeignKey("catalogs_constant.id"), nullable=False, default=0, doc="Camper"
    )
    medication_authorization = Column(String(60), nullable=False)
    event_description = Column(Text)
    camp_restriction = Column(Text)
    administered_medications = Column(Text)
    medical_monitoring = Column(Text)
    comment = Column(Text)
    medical_comment = Column(Text)
    send_in_email = Column(Boolean, nullable=False)
    already_sent = Column(Boolean, nullable=False)
    camp_id = Column(
        "camp", 
        ForeignKey("camps_camp.id"), 
        nullable=True, 
        doc="Campamento"
    )
    camper_id = Column(
        "camper",
        ForeignKey("campers_camper.id"),
        nullable=True,
        doc="Camper",
    )
    initial_visit_id = Column(
        "medical_camper_visit",
        ForeignKey("medical_campermedicalvisit.id"),
        nullable=True,
        doc="Medical Camper Visit",
    )
    created_at = Column("created",DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
