import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Date, ForeignKey, Integer, String, SmallInteger, Float, Text, Date, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID

from model.catalogs.constant import Constant

from utils.db import Base


class Staff(Base):
    __tablename__ = 'staff_staff'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc='id del staff')
    name = Column(String(512), nullable=False)
    lastname_father = Column(String(512), nullable=False)
    lastname_mother = Column(String(512))
    photo = Column(String(512))
    curp = Column(String(100), nullable=False)
    rfc = Column(String(100))
    cellphone = Column(String(30), nullable=False)
    home_phone = Column(String(30), nullable=False)
    birthday = Column(Date, nullable=False)
    affliction = Column(Text)
    blood_type = Column(String(50))
    drug_allergies = Column(Text)
    other_allergies = Column(Text)
    nocturnal_disorders = Column(Text)
    phobias = Column(Text)
    drugs = Column(Text)
    prohibited_foods = Column(Text)
    bio = Column(Text, nullable=False)
    comments = Column(Text)
    employee = Column(Boolean, nullable=False)
    coordinator = Column(Boolean, nullable=False)
    cv = Column(String(512))
    facebook = Column(String(50), nullable=False)
    staff_contact_name = Column(String(512))
    staff_contact_relation = Column(String(512))
    staff_contact_homephone = Column(String(512))
    staff_contact_cellphone = Column(String(512))
    employee_email_send = Column(Boolean, nullable=False)
    login_id = Column(ForeignKey("user.id"), nullable=False, default=0, doc='Usuario')
    record_id = Column(Integer)
    season_id = Column(ForeignKey("camps_season.id"), nullable=False, default=0, doc='Temporada')

    created_at = Column("created",DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )