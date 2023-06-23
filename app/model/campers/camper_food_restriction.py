from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base


class CamperFoodRestriction(Base):
    __tablename__ = "campers_camper_food_restriction"
    __table_args__ = (
        UniqueConstraint('food_restriction_id', 'camper_id'),
    )

    id = Column(
        "id",
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    camper_id = Column("camper_id", ForeignKey("campers_camper.id", ondelete="cascade"))
    food_restriction_id = Column(
        "food_restriction_id", ForeignKey("catalogs_food_restriction.id")
    )
    is_active = Column("is_active", Boolean, doc="Seleccionada por el camper")

