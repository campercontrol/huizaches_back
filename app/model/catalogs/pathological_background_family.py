import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class PathologicalBackgroundFamily(Base):
    __tablename__ = "pathological_background_family"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name_path_back_fam = Column(String(150), default='')
    assigned = Column(SmallInteger(), default='0')
    order = Column(Integer(), default='1')
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
