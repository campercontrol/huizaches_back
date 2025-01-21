import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class TrainingCampaign(Base):
    __tablename__ = 'mailing_training_campaign'
    __table_args__ = (
        UniqueConstraint('campaign_id', 'training_id'),
    )
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id del template para email")
    campaign_id = Column(ForeignKey("mailing_campaign.id", ondelete="cascade"), nullable=False, doc="Campaña de mail")
    training_id = Column(ForeignKey("camps_training.id",  ondelete="cascade"), nullable=False)
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )