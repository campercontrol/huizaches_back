from datetime import datetime
from pydantic import BaseModel

class GroupingCamperBase(BaseModel):
    camper_id: int
    grouping_camp_id: int

class GroupingCamperCreate(GroupingCamperBase):
    pass

class GroupingCamperUpdate(GroupingCamperBase):
    pass
