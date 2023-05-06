from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from xmlrpc.client import boolean

from schema.catalogs.vaccine_schema import VaccineCreate

from pydantic import BaseModel, Field

class CamperExtraAnswerCreate(BaseModel):
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
    answer:str = Field(
        title="Respuesta"
    )
    camper_id:int = Field(
        title="Camper"
    )
    question_id:int = Field(
        title="Pregunta extra"
    )
    created_at:Optional[datetime] = Field(
        default=datetime.now()
    )

class CamperExtraAnswerModify(BaseModel):
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
    answer:str = Field(
        title="Respuesta"
    )
    camper_id:int = Field(
        title="Camper"
    )
    question_id:int = Field(
        title="Pregunta extra"
    )
    updated_at:Optional[datetime] = Field(
        default=datetime.now()
    )

