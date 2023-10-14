import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class Parent(Base):
    __tablename__ = 'campers_parent'

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id del titular de la cuenta")
    user_id= Column(ForeignKey('user.id'), nullable=False, default=0, doc='usuario')
    toku_id = Column(String(512), doc="Id de toku")
    tutor_name = Column(String(512), nullable=False, doc="Nombre")
    tutor_lastname_father = Column(String(512), nullable=False, doc="Primer apellido")
    tutor_lastname_mother = Column(String(512), doc="Segundo apellido")
    tutor_cellphone = Column(String(30), nullable=False, doc="Telefono celular")
    tutor_home_phone = Column(String(30), doc="Telefono de casa")
    tutor_work_phone = Column(String(30), doc="Telefono de trabajo")
    contact_name = Column(String(512), nullable=False, doc="Nombre segundo tutor")
    contact_lastname_father = Column(String(512), nullable=False, doc="Primer apellido segundo tutor")
    contact_lastname_mother = Column(String(512), doc="Segundo apellido segundo tutor")
    contact_cellphone = Column(String(30), nullable=False, doc="Telefono celular segundo tutor")
    contact_home_phone = Column(String(30), doc="Telefono de casa segundo tutor")
    contact_work_phone = Column(String(30), doc="Telefono de trabajo esgundo tutor")
    contact_email = Column(String(75), doc="Email segundo tutor")
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )