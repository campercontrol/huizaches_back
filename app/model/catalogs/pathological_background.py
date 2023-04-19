import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger
from sqlalchemy.dialects.postgresql import UUID

from model.catalogs.constant import Constant

from utils.db import Base

class PathologicalBackground(Base):
    __tablename__ = "catalogs_pathological_background"
    #catalogs_pathological_background en cc2

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    name = Column("name", String(512), default='', nullable=False, doc='Nombre')
    assigned_id = Column("assigned", ForeignKey("catalogs_constant.id"), nullable=False, default=0, doc='mostrar a')
    order = Column("order", Integer(), default='1', nullable=False, doc='orden para mostrar')
    created_at = Column("created",DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )