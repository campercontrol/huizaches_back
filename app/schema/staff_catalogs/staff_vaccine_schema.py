from datetime import date, datetime, datetime
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from pydantic import BaseModel, Field

class StaffVaccineCreate(BaseModel):
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
     
    staff_id:int = Field(
        title='Staff id',
    )
    vaccine_id:int = Field(
        title='Vaccine id',
    )
    is_active: bool = Field(
        title='ACtivo en el staff'
    )
    created_at:Optional[datetime] = Field(
        default=datetime.now()
    )

class StaffVaccineModify(BaseModel):
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
     
    staff_id:int = Field(
        title='Staff id',
    )
    vaccine_id:int = Field(
        title='Vaccine id',
    )
    is_active: bool = Field(
        title='ACtivo en el staff'
    )
    updated_at:Optional[datetime] = Field(
        default=datetime.now()
    )