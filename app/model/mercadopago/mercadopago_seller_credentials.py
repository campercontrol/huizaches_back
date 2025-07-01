from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
    Integer,
    String
)
from utils.db import Base
class MercadopagoSellerCredentials(Base):
    __tablename__ = "mercadopago_cresdentials"
    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    access_token = Column("access_token", String(255))
    token_type = Column("client_id", String(255))
    expires_in = Column("expires_in", Integer)
    scope = Column("scope", String(255))
    user_id = Column("user_id", Integer)
    refresh_token = Column("refresh_token", String(255))
    public_key = Column("public_key", String(255))
    live_mode = Column("live_mode", Boolean)
    created_at = Column("created", DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
