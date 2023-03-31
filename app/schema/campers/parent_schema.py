from datetime import datetime
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from pydantic import BaseModel, Field

class ParentCreate(BaseModel):
    id:int = Field(
        title="Id",
    ) 
    tutor_name:str = Field(
        title="Nombre",
    ) 
    tutor_lastname_father:str = Field(
        title="Primer Apellido",
    ) 
    tutor_lastname_mother: Optional[str] = Field(
        title="Segundo Apellido",
    ) 
    tutor_cellphone:str = Field(
        title="Celular",
    ) 
    tutor_home_phone: Optional[str] = Field(
        title="Telefono de casa",
    ) 
    tutor_work_phone: Optional[str] = Field(
        title="Telefono de trabajo",
    ) 
    contact_name:str = Field(
        title="Nombre del segundo tutor",
    ) 
    contact_lastname_father:str = Field(
        title="Primer apellido del segundo tutor",
    ) 
    contact_lastname_mother: Optional[str] = Field(
        title="Segundo apellido del segundo tutor",
    ) 
    contact_cellphone:str = Field(
        title="Celular del segundo tutor",
    ) 
    contact_home_phone: Optional[str] = Field(
        title="Telefono de casa del segundo tutor",
    ) 
    contact_work_phone: Optional[str] = Field(
        title="Telefono de trabajo del segundo tutor",
    ) 
    contact_email:str = Field(
        title="Email del segundo tutor",
    ) 
    created_at:datetime = Field(
        default=datetime.now()
    )

class ParentModify(BaseModel):
    id:int = Field(
        title="Id",
    ) 
    tutor_name:str = Field(
        title="Nombre",
    ) 
    tutor_lastname_father:str = Field(
        title="Primer Apellido",
    ) 
    tutor_lastname_mother: Optional[str] = Field(
        title="Segundo Apellido",
    ) 
    tutor_cellphone:str = Field(
        title="Celular",
    ) 
    tutor_home_phone: Optional[str] = Field(
        title="Telefono de casa",
    ) 
    tutor_work_phone: Optional[str] = Field(
        title="Telefono de trabajo",
    ) 
    contact_name:str = Field(
        title="Nombre del segundo tutor",
    ) 
    contact_lastname_father:str = Field(
        title="Primer apellido del segundo tutor",
    ) 
    contact_lastname_mother: Optional[str] = Field(
        title="Segundo apellido del segundo tutor",
    ) 
    contact_cellphone:str = Field(
        title="Celular del segundo tutor",
    ) 
    contact_home_phone: Optional[str] = Field(
        title="Telefono de casa del segundo tutor",
    ) 
    contact_work_phone: Optional[str] = Field(
        title="Telefono de trabajo del segundo tutor",
    ) 
    contact_email:str = Field(
        title="Email del segundo tutor",
    ) 
    updated_at:datetime = Field(
        default=datetime.now()
    )