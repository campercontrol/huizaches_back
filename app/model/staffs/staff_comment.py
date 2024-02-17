import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class StaffComment(Base):
    __tablename__ = 'staff_staffcomment'

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id del comentario para el staff")
    comment = Column(Text)
    is_public = Column(Boolean, nullable=False)
    show_to = Column(ForeignKey('catalogs_constant.id'), nullable=False, default=0, doc='mostrar a')
    staff_id = Column(ForeignKey("staff_staff.id"), nullable=False, default=0, doc='Staff')
    user_id = Column(ForeignKey('user.id'), nullable=False, default=0, doc='usuario')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )