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
    role_id: Optional[UUID] = Field(
        title="Id role",
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
    role_id: Optional[UUID] = Field(
        title="Id role",
    )
    is_active: Optional[bool] = Field(
        title="Is active",
    )
    is_superuser: Optional[bool] = Field(
        title="Is superuser",
    )


class UserResetPassword(BaseModel):
    email: EmailStr = Field(
        title="Email",
    )


class UserChangePassword(BaseModel):
    access_token: str
    password: str
    password_confirm: str
