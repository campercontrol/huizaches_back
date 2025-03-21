from datetime import datetime
from pydantic import BaseModel

class GroupingCampBase(BaseModel):
    maximum_capacity: int
    camp_id: int
    grouping_id: int
    
    class Config:
        orm_mode = True

class GroupingCampCreate(GroupingCampBase):
    pass

class GroupingCampUpdate(GroupingCampBase):
    pass

class GroupingCampResponse(GroupingCampBase):
    id: int