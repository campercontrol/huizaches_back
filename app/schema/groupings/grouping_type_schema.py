from datetime import datetime
from pydantic import BaseModel

class GroupingTypeBase(BaseModel):
    name: str

class GroupingTypeCreate(GroupingTypeBase):
    pass

class GroupingTypeUpdate(GroupingTypeBase):
    pass
