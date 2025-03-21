import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class CampCampaign(Base):
    __tablename__ = 'mailing_camp_campaign'
    __table_args__ = (
        UniqueConstraint('camp_id', 'campaign_id'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    campaign_id = Column(ForeignKey("mailing_campaign.id", ondelete="cascade"), nullable=False, doc="Campaña de mail")
    camp_id = Column(ForeignKey("camps_camp.id"), nullable=False, doc="Campamento")

    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )