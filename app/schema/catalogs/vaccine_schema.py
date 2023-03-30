from datetime import date, datetime, datetime
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from pydantic import BaseModel, Field


class VaccineCreate(BaseModel):

    id: Optional[int] = Field(
        title="id"        
    )
    name:str = Field(
        title='Nombre de la vacuna',
        max_length=150,
    )
    assigned_id:int
    order:int
    created_at:datetime = Field(
        default=datetime.now()
    )

class VaccineModify(BaseModel):
   
    name:str = Field(
        title='Nombre de la vacuna',
        max_length=150,
    )
    assigned_id:int
    order:int
    updated_at:datetime = Field(
        default=datetime.now()
    )
    