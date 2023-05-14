import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class CampCheckpoint(Base):
    __tablename__ = 'camps_checkpoint'
    __table_args__ = (
        UniqueConstraint('camp_id', 'name'),
    )

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id del checkpoint")
    name = Column(String(512), nullable=False)
    chekpoint_date = Column("date", Date, nullable=False)
    order = Column(Integer, nullable=False)
    camp_id = Column(ForeignKey("camps_camp.id"), nullable=False, default=0, doc='Campamento')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
