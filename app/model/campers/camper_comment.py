import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class CamperComment(Base):
    __tablename__ = 'campers_campercomment'
    
    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id de la escuela")
    comment = Column(Text)
    is_public = Column(Boolean, nullable=False)
    show_to = Column(ForeignKey("role.id"), nullable=False, default=0, doc="roles")
    camp_id = Column(ForeignKey("camps_camp.id"), nullable=False, default=0, doc='Campamento')
    camper_id = Column(ForeignKey("campers_camper.id"), nullable=False, default=0, doc='Camper')
    user_id = Column(ForeignKey('user.id'), nullable=False, default=0, doc='usuario')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )