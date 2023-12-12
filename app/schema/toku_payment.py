from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class CustomerTokuCreate(BaseModel):
    external_id : Optional[str] = Field(
        title="Id externo",
    )
    email : Optional[EmailStr] = Field(
        title="Email",
    )
    name : Optional[str] = Field(
        title="Nombre del cliente",
    )
    phone : Optional[str] = Field(
        title="Telefono con codigo de lada",
    )
    send_mail : Optional[bool] = Field(
        title="Si se envia correo",
        default=False
    )




class InvoiceTokuCreate(BaseModel):
    customer_id: Optional[str] = Field(
        title="customer_id",
    )
    product_id: Optional[str] = Field(
        default=None,
        title="product_id"
    )
    due_date: Optional[str] = Field(
        default=None,
        title="Fecha limite de la duda"
    )
    amount: Optional[str] = Field(
        default=None,
        title="amount"
    )



class WebhookTokuCreate(BaseModel):
    enabled_events: Optional[list] = Field(
        title="customer_id",
    )
    status: Optional[str] = Field(
        default=None,
        title="product_id"
    )
    url: Optional[str] = Field(
        default=None,
        title="Fecha limite de la duda"
    )


class PaymentsConsultTokuCreate(BaseModel):
    page: Optional[int] = Field(
        title="page",
    )
    page_size: Optional[int] = Field(
        title="page_size"
    )
    start_date: Optional[str] = Field(
        title="start_date"
    )
    end_date: Optional[str] = Field(
        title="end_date"
    )


