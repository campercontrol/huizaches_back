import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class Campaign(Base):
    __tablename__ = 'mailing_campaign'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id de las campañas para email")
    name = Column(String(150), nullable=False)
    camp_parents = Column(Boolean)
    camp_staff = Column(Boolean)
    camp_school = Column(Boolean)
    active_time = Column(String(10))
    send = Column(Boolean, nullable=False)
    camp_id = Column(ForeignKey("camps_camp.id"), doc='Campamento')
    season_id = Column(ForeignKey("camps_season.id"), doc='Temporada')
    send_type_id = Column(ForeignKey("catalogs_constant.id"), nullable=False, default=0, doc='Tipo de campaña')
    training_event_id = Column(ForeignKey("camps_training.id"), doc='Capacitación')
    template_id = Column(ForeignKey("mailing_emailtemplate.id"), nullable=False, default=0, doc='Template')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )