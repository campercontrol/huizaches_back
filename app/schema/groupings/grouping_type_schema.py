from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class GroupingTypeBase(BaseModel):
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

class GroupingTypeUpdate(GroupingTypeBase):
    name: str = Field (
        title='Nombre de la agrupación',
        default=None
    )
class GroupingTypeResponse(GroupingTypeBase):
    name:str
    id:int
    updated_at:datetime
    created_at:datetime    
