from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class GroupingBase(BaseModel):
    name: str
    is_active: bool
    class Config:
        orm_mode = True

class GroupingGet(GroupingBase):
    id: int
    grouping_type_id: int

class GroupingCreate(GroupingBase):
    name:str = Field(
        title="Nombre de la agrupación",
        min_length=1,
        max_length=50
    )
    is_active:bool = Field(
        title="Agrupación activa o inactiva"
    )
    grouping_type_id:int = Field(
        title="Id del tipo de la agrupación"

    )

class GroupingUpdate(GroupingBase):
    name:str = Field(
        title="Nombre de la agrupación",
        min_length=1,
        max_length=50
    )
    is_active:Optional[bool]
    grouping_type_id:Optional[int]

    updated_at:datetime = Field(
        default=datetime.now()
    )
