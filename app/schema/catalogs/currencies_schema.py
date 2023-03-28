from datetime import date
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from pydantic import BaseModel, Field


class CurrenciesCreate(BaseModel):
    name_currency:str = Field(
        default='',
        title='Nombre de la divisa',
        max_length=150,
    )
    symbol:str= Field(
        default='',
        title='Simbolo de la divisa',
        max_lenght=10,
    )
    acronyms:str= Field(
        default='',
        title='Siglas',
        max_lenght= 10,
    )


class CurrenciesModify(BaseModel):
    name_currency:str = Field(
        default='',
        title='Nombre de la divisa',
        max_length=150,
    )
    symbol:str= Field(
        default='',
        title='Simbolo de la divisa',
        max_lenght=10,
    )

    acronyms:str= Field(
        default='',
        title='Siglas',
        max_lenght= 10,
    )