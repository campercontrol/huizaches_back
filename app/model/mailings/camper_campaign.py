import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class CamperCampaign(Base):
    __tablename__ = 'mailing_camper_campaign'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id del template para email")
    campaign_id = Column(ForeignKey("mailing_campaign.id", ondelete="cascade"), doc="Campaña de mail")
    camp_id = Column(ForeignKey("camps_camp.id"), doc="Campamento")
    camper_id = Column(ForeignKey("campers_camper.id", ondelete="cascade"), doc="Camper")

    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )