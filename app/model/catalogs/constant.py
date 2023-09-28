import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, SmallInteger
from sqlalchemy.dialects.postgresql import UUID



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






