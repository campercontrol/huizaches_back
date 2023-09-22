import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class EmailTemplate(Base):
    __tablename__ = 'mailing_emailtemplate'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id del template para email")
    template_type = Column(ForeignKey("catalogs_constant.id"), nullable=False, default=0, doc='Tipo de template')
    title = Column(String(512), nullable=False)
    template = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )