from typing import Optional

from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    name: Optional[str] = Field(
        title="Name",
        max_length=30,
    )


class RoleModify(BaseModel):
    name: Optional[str] = Field(
        title="Name",
        max_length=30,
    )
    is_active: Optional[bool] = Field(
        title="Is active",
    )
