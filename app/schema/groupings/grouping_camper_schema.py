from datetime import datetime
from pydantic import BaseModel

class GroupingCamperBase(BaseModel):
    camper_id: int
    grouping_camp_id: int

    class Config:
        orm_mode = True
 
class GroupingAvailableCampers(BaseModel):
    id: int
    name: str
    birthday: datetime
    gender: str
    class Config:
        orm_mode = True

class GroupingCamperCreate(GroupingCamperBase):
    pass

class GroupingCamperUpdate(GroupingCamperBase):
    pass

class GroupingCamperResponse(GroupingCamperBase):
    id:int
    # created:datetime
    # updated:datetime