from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: Optional[EmailStr] = Field(
        title="Email",
    )
    passw: Optional[str] = Field(
        default=None,
        title="Password",
        max_length=200,
    )
    role_id: Optional[int] = Field(
        title="Id role",
    )
    is_coordinator: Optional[bool] = Field(
        title="Is Coordinator",
    )
    is_admin: Optional[bool] = Field(
        title="Is Admin",
    )
    is_employee: Optional[bool] = Field(
        title="Is Employee",
    )
    is_superuser: Optional[bool] = Field(
        title="Is superuser",
    )


class UserModify(BaseModel):
    email: Optional[EmailStr] = Field(
        title="Email",
    )
    passw: Optional[str] = Field(
        default=None,
        title="Password",
        max_length=200,
    )
    role_id: Optional[int] = Field(
        title="Id role",
    )
    is_coordinator: Optional[bool] = Field(
        title="Is Coordinator",
    )
    is_admin: Optional[bool] = Field(
        title="Is Admin",
    )
    is_employee: Optional[bool] = Field(
        title="Is Employee",
    )
    is_superuser: Optional[bool] = Field(
        title="Is superuser",
    )
    is_active: Optional[bool] = Field(
        title="Is active",
    )


class UserResetPassword(BaseModel):
    email: EmailStr = Field(
        title="Email",
    )


class UserChangePassword(BaseModel):
    access_token: str
    password: str
    password_confirm: str
