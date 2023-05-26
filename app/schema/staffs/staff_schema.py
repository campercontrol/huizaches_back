from datetime import datetime, date
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from pydantic import BaseModel, Field, AnyUrl, condecimal

class ProspectCreate(BaseModel):
   
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
    name: str = Field(
        title= "Numero de transacción",
        max_lenght= 50       
    )
    lastname_father: str = Field(
        title= "Numero de transacción",
        max_lenght= 50       
    )
    lastname_mother: Optional[str] = Field(
        title= "Numero de transacción",
        max_lenght= 50       
    )
    birthday: date = Field(
        title="Fecha de nacimiento"
    )
    curp: str = Field(
        title= "CURP",
        max_lenght= 25       
    )
    bio: str= Field(
        title= "Biografia"
    )
    photo: str = Field(
        title= "Fotografía"
    )
    cellphone: str = Field(
        title="Celular",
        max_lenght=20
    )
    home_phone: str = Field(
        title="Telefono de casa",
        max_lenght=20
    )
    facebook: str = Field(
        title="Facebook",
        max_lenght=25
    )
    created_at:Optional[datetime] = Field(
        default=datetime.now()
    )


class StaffCreate(BaseModel):
   
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
    paid: bool = Field(
        title="Pagado"
    )
    payment_amount: condecimal(decimal_places= 2)
    
    payment_date: date = Field(
        title = "Fecha del pago"
    )
    txn_number: str = Field(
        title= "Numero de transacción",
        max_lenght= 150       
    )    
    camp_id: int = Field(
        title="Camp"
    )
    camper_id: int = Field(
        title="Camper"
    )
    currency_id: int = Field(
        title="Divisa"
    )
    parent_id: int = Field(
        title="Titular de la cuenta"
    )
    payment_method_id: int = Field(
        title="Metodo de pago"
    )
    txn_type_id: int = Field(
        title="Tipo de transacción"
    ) 
    created_at:Optional[datetime] = Field(
        default=datetime.now()
    )


class StaffModify(BaseModel):
    
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
    paid: bool = Field(
        title="Pagado"
    )
    payment_amount: condecimal(decimal_places= 2)
    
    payment_date: date = Field(
        title = "Fecha del pago"
    )
    txn_number: str = Field(
        title= "Numero de transacción",
        max_lenght= 150       
    )    
    camp_id: int = Field(
        title="Camp"
    )
    camper_id: int = Field(
        title="Camper"
    )
    currency_id: int = Field(
        title="Divisa"
    )
    parent_id: int = Field(
        title="Titular de la cuenta"
    )
    payment_method_id: int = Field(
        title="Metodo de pago"
    )
    txn_type_id: int = Field(
        title="Tipo de transacción"
    ) 
    updated_at:Optional[datetime] = Field(
        default=datetime.now()
    )
