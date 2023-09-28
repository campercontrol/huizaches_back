from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base


class StaffFoodRestriction(Base):
    __tablename__ = 'staff_staff_food_restriction'
    __table_args__ = (
        UniqueConstraint('staff_id', 'food_restriction_id'),
    )

    id = Column(
        "id",
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    staff_id = Column('staff_id', ForeignKey('staff_staff.id', ondelete="cascade"))
    food_restriction_id = Column(
        "food_restriction_id", ForeignKey("catalogs_food_restriction.id")
    )
    is_active = Column("is_active", Boolean, doc="Seleccionada por el staff")