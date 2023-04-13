from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table

from utils.db import Base


class CamperPathologicalBackgroundFamily(Base):
    __tablename__ = "campers_camper_pathological_background_family"

    id = Column(
        'id',
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    camper_id = Column('camper_id', ForeignKey('campers_camper.id'))
    pathological_background_family_id = Column('pathological_background_family_id', ForeignKey('catalogs_pathological_background_family.id'))
    is_active = Column('is_active', Boolean, doc='Seleccionada por el camper')
