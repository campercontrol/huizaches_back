from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class GroupingTypeBase(BaseModel):
    id: Optional[int] = Field(
        title="Id",
        default = None,
        primary_key=True
    )
    name: str = Field (
        title='Nombre de la agrupación'
    )
    class Config:
        orm_mode = True

class GroupingTypeCreate(GroupingTypeBase):
    name: str = Field (
        title='Nombre de la agrupación',
        min_length=1
    )

class GroupingTypeUpdate(BaseModel):
    name: str = Field (
        title='Nombre de la agrupación',
        default=None
    )
    
