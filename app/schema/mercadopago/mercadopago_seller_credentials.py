from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class MercadopagoSellerCredentials(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    user_id: int
    refresh_token: str
    public_key: str
    live_mode: bool