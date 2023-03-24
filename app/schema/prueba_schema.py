from datetime import date
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from pydantic import BaseModel, Field


class PruebaCreate(BaseModel):
    name_prueba: Optional[str] = Field(
        default=None,
        title="name_prueba",
        max_length=60,
    )


class PruebaModify(BaseModel):
    name_prueba: Optional[str] = Field(
        default=None,
        title="name_prueba",
        max_length=60,
    ) 
    is_active: Optional[boolean] = Field(
        title="Is Active",
    )