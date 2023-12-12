import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from model.campers.camper import Camper


from utils.db import Base

class Constant(Base):
    __tablename__ = "catalogs_constant"

    uid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        index=True,
    )
    id =Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    value=Column("value", String(512), doc="valor a mostrar")
    num_id = Column("name", Integer(), default=0, nullable=False, doc='Numero de constante')
    language=Column("language", String(2), default="es", doc="Idioma de la constante")    
    model_name=Column(String())

    created_at = Column("created",DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow, 
    )
    catalogs_vaccine = relationship("Vaccine", backref="catalogs_constant", cascade="all, delete-orphan")
    catalogs_pathological_background = relationship("PathologicalBackground", backref="catalogs_constant", cascade="all, delete-orphan")
    catalogs_pathological_background_family = relationship("PathologicalBackgroundFamily", backref="catalogs_constant", cascade="all, delete-orphan")
    catalogs_licensed_medicine = relationship("LicensedMedicine", backref="catalogs_constant", cascade="all, delete-orphan")
    catalogs_food_restriction = relationship("FoodRestriction", backref="catalogs_constant", cascade="all, delete-orphan")
    camps_camperincamp = relationship("CamperInCamp", backref="catalogs_constant", cascade="all, delete-orphan")
    mailing_campaign = relationship("Campaign", backref="catalogs_constant", cascade="all, delete-orphan")
    mailing_emailtemplate = relationship("EmailTemplate", backref="catalogs_constant", cascade="all, delete-orphan")
    staff_staffcomment = relationship("StaffComment", backref="catalogs_constant", cascade="all, delete-orphan")
    staff_staff = relationship("Staff", backref="catalogs_constant", cascade="all, delete-orphan")
    trophy_trophy = relationship("Trophy", backref="catalogs_constant", cascade="all, delete-orphan")
    # foreign_keys=["campers_camper.gender_id","campers_camper.grade","campers_camper.can_swim","campers_camper.blood_type"]
    # campers_camper_gender = relationship("Camper", foreign_keys = [Camper.gender_id] ,backref="catalogs_constant", cascade="all, delete-orphan")
    # campers_camper_grade = relationship("Camper", foreign_keys = [Camper.grade], backref="catalogs_constant", cascade="all, delete-orphan")
    # campers_camper_can_swim = relationship("Camper", foreign_keys = [Camper.can_swim] , backref="catalogs_constant", cascade="all, delete-orphan")
    # campers_camper_blood_type = relationship("Camper", foreign_keys = [Camper.blood_type] , backref="catalogs_constant", cascade="all, delete-orphan")
     




    def __repr__(self):
        return f"{self.uid} - {self.id} - {self.value} - {self.num_id} - {self.language} - {self.model_name} - {self.created_at} - {self.updated_at}"

#1    masculino  1    es     gender
#2    femenino   2    es     gender
#3    no_binario 3    es     gender
#4    male       1    en     gender
#5    female     2    en     gender
#6    non binary 3    en     gender
#7    A+         1
#8    A-         2
#9    B+         3
#10   B-         
#11
#
#
#Pavel Trejo .... 1
#Pavel Trejo .... 1
#
#
#
#Class Gender():
#
#    id=
#    name_es=
#    name_en=
#    name_fr=
#






