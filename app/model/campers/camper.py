#import uuid
#from datetime import datetime
#
#from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger, Float, Text, Date
#from sqlalchemy.dialects.postgresql import UUID
#
#
#
#from utils.db import Base
#
#class Camper(Base):
#    __tablename__ = 'campers_camper'
#
#    id = Column(Integer, primary_key=True, server_default=text("nextval('campers_camper_id_seq'::regclass)"))
#    name = Column(String(512), nullable=False)
#    lastname_father = Column(String(512), nullable=False)
#    photo = Column(String(512))
#    lastname_mother = Column(String(512), nullable=False)
#    gender = Column(String(20), nullable=False)
#    birthday = Column(Date, nullable=False)
#    height = Column(Float(53))
#    weight = Column(Float(53))
#    grade = Column(Integer, nullable=False)
#    school_other = Column(String(512))
#    email = Column(String(75))
#    can_swim = Column(String(10), nullable=False)
#    affliction = Column(Text)
#    blood_type = Column(String(512), nullable=False)
#    heart_problems = Column(Text)
#    psicology_treatments = Column(Text)
#    prevent_activities = Column(Text)
#    drug_allergies = Column(Text)
#    other_allergies = Column(Text)
#    nocturnal_disorders = Column(Text)
#    phobias = Column(Text)
#    drugs = Column(Text)
#    doctor_precall = Column(Boolean, nullable=False)
#    prohibited_foods = Column(Text)
#    comments_admin = Column(Text)
#    insurance = Column(Boolean, nullable=False)
#    insurance_company = Column(String(512))
#    insurance_number = Column(String(512))
#    security_social_number = Column(String(512))
#    contact_name = Column(String(512))
#    contact_relation = Column(String(512))
#    contact_homephone = Column(String(512))
#    contact_cellphone = Column(String(512))
#    parent_id = Column(Integer, index=True)
#    record_id = Column(Integer, index=True)
#    school_id = Column(Integer, index=True)
#
#    created_at = Column("created",DateTime(timezone=True), default=datetime.utcnow)
#    updated_at = Column(
#        "updated",
#        DateTime(timezone=True),
#        default=datetime.utcnow,
#        onupdate=datetime.utcnow,
#    )
#