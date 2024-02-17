from datetime import datetime, date
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from pydantic import BaseModel, Field, AnyUrl, condecimal

class CamperExtraChargeCreate(BaseModel):
   
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
    is_selected:bool = Field(
        title= "Nombre del metodo de pago"
    )
    camper_id:int = Field(
        title="Camper"
    )
    extra_charge_id:int = Field(
        title="Cargo Extra"
    )
    created_at:Optional[datetime] = Field(
        default=datetime.now()
    )


class CamperExtraChargeModify(BaseModel):
    
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
    is_selected:bool = Field(
        title= "Nombre del metodo de pago"
    )
    camper_id:int = Field(
        title="Camper"
    )
    extra_charge_id:int = Field(
        title="Cargo Extra"
    )
    updated_at:Optional[datetime] = Field(
        default=datetime.now()
    )

class ExtraChargeListCreate(BaseModel):
    extra_charge_id:int = Field(
        title="Cargo Extra Id"
    )
    extra_charge_name: str = Field(
        title="Nombre del cargo extra"
    )
    extra_charge_price: int = Field(
        title= "Precio del cargo extra"
    )
    extra_selected:bool = Field(
        title= "Nombre del metodo de pago"
    )
    camper_id:int = Field(
        title="Camper"
    )
    

class CamperExtraChargeListCreate(BaseModel):
    extra_charges: list[ExtraChargeListCreate]

class ExtraChargeMultiple(BaseModel):
    
    camp_extra_charge_is_selected:bool = Field(
        title="Seleccionado"
    )

    camp_extra_charge_id:int = Field(
        title = "Cargo extra id"
    )
