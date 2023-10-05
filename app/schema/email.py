from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class EmailWebhookCreate(BaseModel):
    type: Optional[str] = Field(
        title="Type of webhook [accepted, clicked, complained, delivered, opened, permanent_fail, temporary_fail, unsubscribed]",
    )
    urls: Optional[list] = Field(
        default=None,
        title="Urls of webhook limit 3"
    )

class WebhookUrl(BaseModel):
    urls: Optional[list] = Field(
        default=None,
        title="Urls of webhook limit 3"
    )