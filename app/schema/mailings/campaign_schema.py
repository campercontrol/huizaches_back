from datetime import date, datetime, datetime
from typing import Optional, List
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

    camp_parents: Optional[boolean]  = Field(
        title="Mandar a titulares de la cuenta"
    )

    camp_staff: Optional[boolean]  = Field(
        title="Mandar a staff"
    )

    camp_school:Optional[boolean]  = Field(
        title="Mandar a el colegio"
    )

    active_time: Optional[str] = Field(
        title="Tiempo para enviar",
        default="1"
    )

    send: boolean  = Field(
        title="Mandar a el colegio"
    )

    camp_id: Optional[int] = Field(
        title="Tipo de template"
    )

    season_id: Optional[int] = Field(
        title="Temporada"
    )

    send_type_id: int = Field(
        title="Tipo de envío"
    )

    training_event_id: Optional[int] = Field(
        title="Capacitación"
    )

    template_id: int = Field(
        title="Template"
    )

    created_at:Optional[datetime] = Field(
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

    camp_parents: Optional[boolean]  = Field(
        title="Mandar a titulares de la cuenta"
    )

    camp_staff: Optional[boolean]  = Field(
        title="Mandar a staff"
    )

    camp_school:Optional[boolean]  = Field(
        title="Mandar a el colegio"
    )

    active_time: Optional[str] = Field(
        title="Tiempo para enviar",
        default="1"
    )

    send: boolean  = Field(
        title="Mandar a el colegio"
    )

    camp_id: Optional[int] = Field(
        title="Tipo de template"
    )

    season_id: Optional[int] = Field(
        title="Temporada"
    )

    send_type_id: int = Field(
        title="Tipo de envío"
    )

    training_event_id: Optional[int] = Field(
        title="Capacitación"
    )

    template_id: int = Field(
        title="Template"
    )

    updated_at: Optional[datetime] = Field(
        default=datetime.now()
    )

class MailingTypeSelect(BaseModel):

    camps_id:List[int] = Field(
        title = "campamentos"
    )
    staffs: bool = Field(
        title= "Se envia a staff"
    )
    campers: bool = Field(
        title= "Se envia a campers"
    )
    schools: bool = Field(
        title= "Se envia a escuelas"
    )
    training_id: int = Field(
        title = "Capacitación"
    )
    season: int = Field(
        title = "Temporada"
    )

    