from datetime import date, datetime, datetime
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from pydantic import BaseModel, Field


class CampaignCreate(BaseModel):

    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 

    name: str = Field(
        title="Nombre de la campaña"
    ) 

    camp_parents: boolean  = Field(
        title="Mandar a titulares de la cuenta"
    )

    camp_staff: boolean  = Field(
        title="Mandar a staff"
    )

    camp_school: boolean  = Field(
        title="Mandar a el colegio"
    )

    active_time: str = Field(
        title="Tiempo para enviar",
        default="1"
    )

    send: boolean  = Field(
        title="Mandar a el colegio"
    )

    camp_id: int = Field(
        title="Tipo de template"
    )

    season_id: int = Field(
        title="Temporada"
    )

    send_type_id: int = Field(
        title="Tipo de envío"
    )

    training_event_id: int = Field(
        title="Capacitación"
    )

    template_id: int = Field(
        title="Template"
    )

    created_at:datetime = Field(
        default=datetime.now()
    )


class CampaignModify(BaseModel):
    
    id:Optional[int] = Field(
        title="Id",
        default=None,
        primary_key=True
    ) 
     
    name: str = Field(
        title="Nombre de la campaña"
    ) 

    camp_parents: boolean  = Field(
        title="Mandar a titulares de la cuenta"
    )

    camp_staff: boolean  = Field(
        title="Mandar a staff"
    )

    camp_school: boolean  = Field(
        title="Mandar a el colegio"
    )

    active_time: str = Field(
        title="Tiempo para enviar",
        default="1"
    )

    send: boolean  = Field(
        title="Mandar a el colegio"
    )

    camp_id: int = Field(
        title="Tipo de template"
    )

    season_id: int = Field(
        title="Temporada"
    )

    send_type_id: int = Field(
        title="Tipo de envío"
    )

    training_event_id: int = Field(
        title="Capacitación"
    )

    template_id: int = Field(
        title="Template"
    )
    
    updated_at:datetime = Field(
        default=datetime.now()
    )