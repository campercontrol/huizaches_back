import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from utils.db import Base

class Currency(Base):
    __tablename__="catalogs_currency"
    #catalogs_currencies en cc2

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True) 
    name = Column("name", String(150), default='', nullable=False, doc='Nombre de la divisa')
    symbol = Column("symbol", String(10), default='', nullable=False, doc='Simbolo de la divisa')
    acronyms = Column("acronyms", String(10), default='', nullable=False, doc='Siglas')
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated", 
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"{self.id} - {self.name} - {self.symbol} - {self.acronyms} - {self.created_at} - {self.updated_at}"