from datetime import datetime
from pydantic import BaseModel

class GroupingBase(BaseModel):
    name: str
    is_active: bool
    grouping_type_id: int

class GroupingCreate(GroupingBase):
    pass

class GroupingUpdate(GroupingBase):
    pass
