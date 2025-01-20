from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey


from utils.db import Base
class StoreStorePayment(Base):
    __tablename__ = 'store_storepayment'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id de store transaction type")
    store_payment_amount = Column(Integer, nullable=False)
    camp_id = Column(ForeignKey("camps_camp.id"), nullable=False)
    camper_id = Column(ForeignKey('campers_camper.id'), nullable=False)
    parent_id = Column(ForeignKey('campers_parent.id'), nullable=False)
    store_type_movement_id = Column(ForeignKey('store_storetransactiontype.id'), nullable=False)
    store_payment_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
