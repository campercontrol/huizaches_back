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

from utils.db import Base
class Doctor(Base):
    __tablename__ = 'medical_doctor'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id Doctor")
    name = Column(String(512), nullable=False)
    lastname_father = Column(String(512), nullable=False)
    lastname_mother = Column(String(512))
    cellphone = Column(String(30), nullable=False)
    login_id = Column(ForeignKey("user.id"), nullable=True,  doc='Usuario')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

