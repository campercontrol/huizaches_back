from pydantic import BaseModel
from typing import Union

class Token(BaseModel):
    access_token: str
    token_type: str
    # refresh_token: str

class TokenData(BaseModel):
    username: Union[str, None] = None



# Temporal Token Fix, please uncomment this code in the next iteration

# class TokenCreate(BaseModel):
#     username: str
#     password: str

class TokenCreate(BaseModel):
    username: str
    password: str
    lang: str



class TokenRefresh(BaseModel):
    access_token: str
    refresh_token: str
