from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base


class CamperPathologicalBackground(Base):
    __tablename__ = "campers_camper_pathological_background"
    __table_args__ = (
        UniqueConstraint('pathological_background_id', 'camper_id'),
    )

    id = Column(
        'id',
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    camper_id = Column('camper_id', ForeignKey('campers_camper.id', ondelete="cascade"))
    pathological_background_id = Column('pathological_background_id', ForeignKey('catalogs_pathological_background.id'))
    is_active = Column('is_active', Boolean, doc='Seleccionada por el camper')
