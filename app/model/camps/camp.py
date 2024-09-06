import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class Camp(Base):
    __tablename__ = 'camps_camp'

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    name = Column(String(512), nullable=False)
    start = Column(DateTime(True), nullable=False)
    end = Column(DateTime(True), nullable=False)
    start_registration = Column(DateTime(True), nullable=False)
    end_registration = Column(DateTime(True), nullable=False)
    registration = Column(Boolean, nullable=False)
    url = Column(String(512))
    special_message = Column(Text)
    special_message_admin = Column(Text)
    public_price = Column(Float(53))
    show_payment_parent = Column(Boolean, nullable=False)
    show_rebate_parent = Column(Boolean, nullable=False)
    show_paypal_button = Column(Boolean, nullable=False)
    show_mercadopago_button = Column(Boolean, nullable=False, default=False)
    recommended_payment_dates = Column(Text)
    show_payment_order = Column(Boolean, nullable=False)
    reminder_camp_days = Column(Integer, nullable=False)
    reminder_discount_days = Column(Integer, nullable=False)
    insurance = Column(Float(53))
    venue = Column(String(250), nullable=False)
    photo_url = Column(String(200))
    photo_password = Column(String(100), nullable=False)
    medical_report = Column(String(512))
    occupancy_camp = Column(Integer)
    active = Column(Boolean, nullable=False)
    general_camp = Column(Boolean, nullable=False)
    currency_id = Column(ForeignKey("catalogs_currency.id"), nullable=True,  doc='Titular de la cuenta')
    location_id = Column(ForeignKey("camps_location.id"), nullable=True, doc='Titular de la cuenta')
    school_id = Column(ForeignKey("campers_school.id"), nullable=True, doc='Titular de la cuenta')
    season_id = Column(ForeignKey("camps_season.id"), nullable=True,  doc='Titular de la cuenta')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
