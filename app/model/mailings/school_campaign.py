import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class SchoolCampaign(Base):
    __tablename__ = 'mailing_school_campaign'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id del template para email")
    campaign_id = Column(ForeignKey("mailing_campaign.id"), doc="Campaña de mail")
    camp_id = Column(ForeignKey("camps_camp.id"), doc="Campamento")
    school_id = Column(ForeignKey("campers_school.id"), doc="Escuela")

    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )