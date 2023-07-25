from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.schema import UniqueConstraint

from utils.db import Base


class StaffVaccine(Base):
    __tablename__ = 'staff_staff_vaccines'
    __table_args__ = (
        UniqueConstraint('staff_id', 'vaccine_id'),
    )

    id = Column(
        'id',
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
        doc='id del camper',
    )
    staff_id = Column('staff_id', ForeignKey('staff_staff.id', ondelete="cascade"))
    vaccine_id = Column('vaccine_id', ForeignKey('catalogs_vaccine.id'))
    is_active = Column('is_active', Boolean, doc='Seleccionada por el staff')