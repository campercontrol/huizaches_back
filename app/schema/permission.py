from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class PermissionCreate(BaseModel):
    name : Optional[str] = Field(
        default=None,
        title="name",
        max_length=200,
    )
    url: Optional[str] = Field(
        default=None,
        title="url",
        max_length=200,
    )
    icon: Optional[str] = Field(
        default=None,
        title="icon",
        max_length=200,
    )
    language: Optional[str] = Field(
        default=None,
        title="language",
        max_length=2,
    )
    is_coordinator : Optional[bool] = Field(
        title="Is Coordinator",
    )
    is_admin: Optional[bool] = Field(
        title="Is Admin",
    )
    is_employee: Optional[bool] = Field(
        title="Is Employee",
    )
    target: Optional[bool] = Field(
        title="target",
    )
    order: Optional[int] = Field(
        title="order",
    )
    role_id: Optional[int] = Field(
        title="Id role",
    )
    new_window : Optional[bool] = Field(
        title="new_window",
    )


class PermissionModify(BaseModel):
    name : Optional[str] = Field(
        default=None,
        title="name",
        max_length=200,
    )
    url: Optional[str] = Field(
        default=None,
        title="url",
        max_length=200,
    )
    icon: Optional[str] = Field(
        default=None,
        title="icon",
        max_length=200,
    )
    language: Optional[str] = Field(
        default=None,
        title="language",
        max_length=2,
    )
    is_coordinator : Optional[bool] = Field(
        title="Is Coordinator",
    )
    is_admin: Optional[bool] = Field(
        title="Is Admin",
    )
    is_employee: Optional[bool] = Field(
        title="Is Employee",
    )
    target: Optional[bool] = Field(
        title="target",
    )
    order: Optional[int] = Field(
        title="order",
    )
    role_id: Optional[int] = Field(
        title="Id role",
    )
    new_window : Optional[bool] = Field(
        title="new_window",
    )
    is_active: Optional[bool] = Field(
        title="Is active",
    )


