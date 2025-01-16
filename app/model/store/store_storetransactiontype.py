from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String


from utils.db import Base
class StoreStoreTransactionType(Base):
    __tablename__ = 'store_storetransactiontype'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc="id de store transaction type")
    name = Column(String(150))
    movement = Column(Integer)
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
