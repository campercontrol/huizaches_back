from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenCreate(BaseModel):
    username: str
    password: str
    lang: str


class TokenRefresh(BaseModel):
    access_token: str
    refresh_token: str
