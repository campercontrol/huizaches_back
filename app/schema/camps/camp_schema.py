from datetime import datetime
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from pydantic import BaseModel, Field, AnyUrl, condecimal

class CampCreate(BaseModel):
   
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
    name: str = Field(
        title="Nombre del campamento",
        max_lenght= 150
    )
    start: datetime = Field(
        title="Inicio del campamento",
        default=datetime.now()
    )
    end: datetime = Field(
        title="Fin del campamento",
        default=datetime.now()
    )
    start_registration: datetime = Field(
        title="Inicio de registro",
        default=datetime.now()
    )
    end_registration: datetime = Field(
        title="Fin de registro",
        default=datetime.now()
    )
    registration: bool = Field(
        title="Registro abierto"
    )
    url: AnyUrl = Field(
        title="Pagina web para mas información",
        max_lenght= 150
    )
    special_message: str = Field(
        title="Mensaje para titulares de la cuenta."
    )
    special_message_admin: str = Field(
        title="Mensaje especial solo visible para administradores"
    )
    public_price:  condecimal(decimal_places= 2)

    show_payment_parent: bool = Field(
        title="Mostrar pago a titulares de la cuenta"
    )
    show_rebate_parent: bool = Field(
        title="Mostrar descuento a titulares de la cuenta"
    )
    show_paypal_button: bool = Field(
        title="Activar boton de paypal para este campamento"
    )
    paypal_button: str = Field(
        title=""
    )
    show_payment_order: bool = Field(
        title="Mostrar orden de pago a titulares de la cuenta"
    )
    reminder_camp_days: int = Field(
        title="Dias antes para recordar del campamento"
    )
    reminder_discount_days: int = Field(
        title="Dias antes para recordar del descuento"
    )
    insurance: condecimal(decimal_places= 2)

    venue: str = Field(
        title="Punto de reunión",
        max_lenght= 150
    )
    photo_url: AnyUrl = Field(
        title="Url para la galeria de fotos"
    )
    photo_password: str = Field(
        title="Contraseña para galeria de fotos"
    )
    medical_report: str = Field(
        title="Reporte medico"
    )
    occupancy_camp: int = Field(
        title="Capacidad maxima del campamento"
    )
    active: bool = Field(
        title="Campamento activo"
    )
    general_camp: bool = Field(
        title="Campamento de verano"
    )
    currency_id: int = Field(
        title="Divisa dentro de campamento"
    )
    location_id: Optional[int] = Field(
        title="Sede del campamento"
    )
    school_id: int = Field(
        title="Escuela del campamento"
    )
    season_id: int = Field(
        title="Temporada del campamento"
    )
    created_at:Optional[datetime] = Field(
        default=datetime.now()
    )


class CampModify(BaseModel):
    
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
    name: str = Field(
        title="Nombre del campamento",
        max_lenght= 150
    )
    start: datetime = Field(
        title="Inicio del campamento",
        default=datetime.now()
    )
    end: datetime = Field(
        title="Fin del campamento",
        default=datetime.now()
    )
    start_registration: datetime = Field(
        title="Inicio de registro",
        default=datetime.now()
    )
    end_registration: datetime = Field(
        title="Fin de registro",
        default=datetime.now()
    )
    registration: bool = Field(
        title="Registro abierto"
    )
    url: AnyUrl = Field(
        title="Pagina web para mas información",
        max_lenght= 150
    )
    special_message: str = Field(
        title="Mensaje para titulares de la cuenta."
    )
    special_message_admin: str = Field(
        title="Mensaje especial solo visible para administradores"
    )
    public_price: condecimal(decimal_places= 2)
    
    show_payment_parent: bool = Field(
        title="Mostrar pago a titulares de la cuenta"
    )
    show_rebate_parent: bool = Field(
        title="Mostrar descuento a titulares de la cuenta"
    )
    show_paypal_button: bool = Field(
        title="Activar boton de paypal para este campamento"
    )
    paypal_button: str = Field(
        title=""
    )
    show_payment_order: bool = Field(
        title="Mostrar orden de pago a titulares de la cuenta"
    )
    reminder_camp_days: int = Field(
        title="Dias antes para recordar del campamento"
    )
    reminder_discount_days: int = Field(
        title="Dias antes para recordar del descuento"
    )
    insurance:  condecimal(decimal_places= 2)
    
    venue: str = Field(
        title="Punto de reunión",
        max_lenght= 150
    )
    photo_url: AnyUrl = Field(
        title="Url para la galeria de fotos"
    )
    photo_password: str = Field(
        title="Contraseña para galeria de fotos"
    )
    medical_report: str = Field(
        title="Reporte medico"
    )
    occupancy_camp: int = Field(
        title="Capacidad maxima del campamento"
    )
    active: bool = Field(
        title="Campamento activo"
    )
    general_camp: bool = Field(
        title="Campamento de verano"
    )
    currency_id: int = Field(
        title="Divisa dentro de campamento"
    )
    location_id: Optional[int] = Field(
        title="Sede del campamento"
    )
    school_id: int = Field(
        title="Escuela del campamento"
    )
    season_id: int = Field(
        title="Temporada del campamento"
    )
    updated_at:Optional[datetime] = Field(
        default=datetime.now()
    )

class PaymentAccount(BaseModel):
    id:int = Field(
        title = "Id de la cuenta"
    )
    name:int = Field(
        title = "Nombre de la cuenta de banco"
    )


class CampPaymentAccountCreate(BaseModel):
    camp : CampCreate
    payment_accounts: Optional[list[PaymentAccount]]