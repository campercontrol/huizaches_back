import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Date, ForeignKey, Integer, String, SmallInteger, Float, Text, Date, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID

from model.catalogs.constant import Constant
from model.campers.parent import Parent
from model.campers.school import School

from utils.db import Base



class Camper(Base):
    __tablename__ = 'campers_camper'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, doc='id del camper')
    name = Column(String(512), nullable=False, doc='Nombre')
    lastname_father = Column(String(512), nullable=False, doc='Primer apellido')
    photo = Column(String(512), nullable=False, doc= 'URL de la foto guardada')
    lastname_mother = Column(String(512), doc='Segundo apellido')
    gender_id = Column(ForeignKey('catalogs_constant.id'), nullable=False, default=0, doc='Genero')
    birthday = Column(Date(), nullable=False, doc='Fecha de nacimiento')
    height = Column(Float(53), nullable=False, doc='Altura')
    weight = Column(Float(53), nullable=False, doc='Peso')
    grade = Column(ForeignKey('catalogs_constant.id'), nullable=False, default=0, doc='Grado escolar')
    school_id = Column(ForeignKey('campers_school.id'), nullable=False, default=0, doc='Escuela')
    school_other = Column(String(512), doc='Otra escuela')
    email = Column(String(75), nullable=False, doc='Email')
    can_swim = Column(ForeignKey('catalogs_constant.id'), nullable=False, default=0, doc='Sabe nadar')
    affliction = Column(Text, nullable=False,doc='Enfermedades')
    blood_type = Column(ForeignKey('catalogs_constant.id'), nullable=False, default=0, doc='Tipo de sangre')
    temporal_blood_type = Column(String(15), doc="Tipo de sangre temporal para la migración")
    #vaccines = relationship("Vaccine", secondary='campers_camper_vaccines', back_populates='campers_camper')
    heart_problems = Column(Text, nullable= False, doc= 'Problemas cardiacos')
    psicology_treatments = Column(Text, nullable= False, doc= 'Tratamientos psicologicos y psiquiatricos')
    prevent_activities = Column(Text, nullable= False, doc='Cirugias, fracturas o esguinces que le impidan realizar actividades ')
    drug_allergies = Column(Text, nullable= False, doc='Alergias a medicamentos')
    other_allergies = Column(Text, nullable= False, doc= 'Otras alergias')
    nocturnal_disorders = Column(Text, nullable= False, doc='Alteraciones nocturnas')
    phobias = Column(Text, nullable=False, doc='Fobias o miedos')
    drugs = Column(Text, nullable=False, doc='Medicamentos')
    doctor_precall = Column(Boolean, nullable=False, doc='Llamada previa del doctor')
    prohibited_foods = Column(Text, nullable= False, doc='Comida prohibida')
    comments_admin = Column(Text, doc='Comentarios del admin')
    insurance = Column(Boolean, doc= 'Cuenta con seguro médico')
    insurance_company = Column(String(512), doc='Compañia de seguros')
    insurance_number = Column(String(512), doc= 'Numero de seguro')
    security_social_number = Column(String(512), doc='Numero de seguro social')
    contact_name = Column(String(512), nullable=False,  doc='Nombre completo del contacto de emergencia')
    contact_relation = Column(String(512), nullable=False,  doc='Relación del camper con el  contacto de emergencia')
    contact_homephone = Column(String(512), nullable=False,  doc='Telefono de casa del contacto de emergencia')
    contact_cellphone = Column(String(512), nullable=False,  doc='Celular del contacto de emergencia')
    parent_id = Column(ForeignKey("campers_parent.id"), nullable=False, default=0, doc='Titular de la cuenta')
    record_id = Column(Integer, index=True, doc='Record de campamentos')
    

    created_at = Column("created",DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        "updated",
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

