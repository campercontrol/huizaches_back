from typing import Optional
from pydantic import BaseModel, Field

class CreateCampPaymentAccount(BaseModel):
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
    camp_id: int = Field(
        title= "ID del campamento"
    )
    paymentaccount_id: int = Field(
        title= "ID del payment account"
    )
    


