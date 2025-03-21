import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base
class ParentCampaign(Base):
    __tablename__ = 'mailing_parent_campaign'
    __table_args__ = (
        UniqueConstraint('parent_id', 'campaign_id'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    campaign_id = Column(ForeignKey("mailing_campaign.id", ondelete="cascade"), nullable=False, doc="Campaña de mail")
    parent_id = Column(ForeignKey("campers_parent.id"), nullable=False, doc="Id del padre")

    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )