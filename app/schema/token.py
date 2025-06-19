from pydantic import BaseModel
from typing import Union

class Token(BaseModel):
    access_token: str
    token_type: str
    # refresh_token: str

class TokenData(BaseModel):
    username: Union[str, None] = None


class TokenCreate(BaseModel):
    username: str
    password: str


class TokenRefresh(BaseModel):
    access_token: str
    refresh_token: str
