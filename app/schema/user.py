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
    is_active: Optional[bool] = Field(
        title="Is active"
    )
class UserCreateAdmin(BaseModel):
    email: EmailStr = Field(
        title="Email",
    )
    passw: str = Field(
        title="Password",
        max_length=200,
    )
    role_id: int = Field(
        title="Id role",
    )
    is_coordinator: Optional[bool] = Field(
        title="Is Coordinator",
        default=False
    )
    is_admin: Optional[bool] = Field(
        title="Is Admin",
        default=False
    )
    is_employee: Optional[bool] = Field(
        title="Is Employee",
        default=False
    )
    is_superuser: Optional[bool] = Field(
        title="Is superuser",
        default=False
    )
    is_active: Optional[bool] = Field(
        title="Is active",
        default= False
    )

class UserModify(BaseModel):
    email: Optional[EmailStr] = Field(
        title="Email",
    )
    hashed_pass: Optional[str] = Field(
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

class UserSendMailResetPassword(BaseModel):
    email: EmailStr = Field(
        title="Email",
    )
class UserResetPassword(BaseModel):
    email: EmailStr = Field(
        title="Email",
    )
    password: str


class UserChangePassword(BaseModel):
    access_token: str
    password: str
    password_confirm: str



class UserChangeEmail(BaseModel):
    access_token: str
    email: str
    email_confirm: str
