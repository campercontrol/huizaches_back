from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base


class CamperLicensedMedicine(Base):
    __tablename__ = "campers_camper_licensed_medicine"
    __table_args__ = (
        UniqueConstraint('licensed_medicine_id', 'camper_id'),
    )

    id = Column(
        "id",
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    camper_id = Column("camper_id", ForeignKey("campers_camper.id"))
    licensed_medicine_id = Column(
        "licensed_medicine_id", ForeignKey("catalogs_licensed_medicine.id")
    )
    is_active = Column("is_active", Boolean, doc="Seleccionada por el camper")
