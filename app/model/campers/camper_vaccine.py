from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base


class CamperVaccine(Base):
    __tablename__ = "campers_camper_vaccines"
    __table_args__ = (
        UniqueConstraint('camper_id', 'vaccine_id'),
    )
    id = Column(
        'id',
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
        doc='id del camper',
    )
    camper_id = Column('camper_id', ForeignKey('campers_camper.id'))
    vaccine_id = Column('vaccine_id', ForeignKey('catalogs_vaccine.id'))
    is_active = Column('is_active', Boolean, doc='Seleccionada por el camper')
