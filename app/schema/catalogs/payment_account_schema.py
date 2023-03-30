from datetime import date, datetime, datetime
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from pydantic import BaseModel, Field


class PaymentAccountCreate(BaseModel):

    id: Optional[int] = Field(
        title="id"        
    )
    name:str = Field(
        title='Valor a mostrar',
        max_length=150,
    )
    bank:str = Field(
        title='Banco de la cuenta',
        max_length=30,
    )
    account_number:str= Field(
        title='Numero de cuenta',
        max_length=10
    )
    clabe_number:str= Field(
        title='Numero clabe',
        max_length=18        
    )
    created_at:datetime = Field(
        default=datetime.now()
    )


class PaymentAccountModify(BaseModel):
    
    id: Optional[int] = Field(
        title="id"        
    )
    name:str = Field(
        title='Valor a mostrar',
        max_length=150,
    )
    bank:str = Field(
        title='Banco de la cuenta',
        max_length=30,
    )
    account_number:str= Field(
        title='Numero de cuenta',
        max_length=10
    )
    clabe_number:str= Field(
        title='Numero clabe',
        max_length=18
    )
    updated_at:datetime = Field(
        default=datetime.now()
    )