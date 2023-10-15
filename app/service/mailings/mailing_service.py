from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.mailings.email_template_crud import (
    get_all_email_template,
    get_all_massive_template,
    get_all_system_template,
)
from crud.mailings.campaign_crud import get_all_campaign
from crud.mailings.mailing_crud import (
    get_sent_camp,
    get_sent_camps,
    get_sent_training,
    get_sent_candidates,
)
from crud.camps.camper_in_camp_crud import get_campers_for_camp
from crud.camps.staff_in_camp_crud import get_staff_in_camp
from crud.training.staff_in_training_crud import get_all_staff_in_training_event
from crud.staffs.staff_crud import get_all_prospect_by_season
from model.mailings import (
    CamperCampaign,
    StaffCampaign,
    SchoolCampaign,
    Campaign,
    EmailTemplate,
)
from model.catalogs import Constant
from schema.mailings.campaign_schema import CampaignSend

from helper.mailing_helpers import send_mail_template

from utils.db import SessionLocal

mailing_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@mailing_routes.get("/mailing/template/massive/", tags=["Mailing"])
def get_email_template_massive(db: Session = Depends(get_db)):
    list_template = get_all_massive_template(db)
    return {"data": list_template}


@mailing_routes.get("/mailing/template/system/", tags=["Mailing"])
def get_email_template_system(db: Session = Depends(get_db)):
    list_template = get_all_system_template(db)
    return {"data": list_template}


@mailing_routes.get("/mailing/campaign/", tags=["Mailing"])
def get_campaign(db: Session = Depends(get_db)):
    list_campaign = get_all_campaign(db)
    return {"data": list_campaign}


@mailing_routes.get("/mailing/campaign/{campaign_id}/", tags=["Mailing"])
def get_campaign_by_id(campaign_id: int, db: Session = Depends(get_db)):
    """
    Tenemos 3 opciones para el envío de correo:

    Si tiene un id: 80 significa un correo enviado a participantes de un campamento

    Si tiene un id: 81 significa un correo enviado a participantes de una capacitación

    Si tiene un id: 82 significa un correo enviado a participantes de varios campamentos

    Si tiene un id: 83 significa un correo enviado a candidatos de alguna temporada
    """
    campaign_type = (
        db.query(Campaign.send_type_id).filter(Campaign.id == campaign_id).first()
    )
    send_type = campaign_type[0]
    if send_type == 80:
        data = get_sent_camp(db, campaign_id)
    elif send_type == 81:
        data = get_sent_training(db, campaign_id)
    elif send_type == 82:
        data = get_sent_camps(db, campaign_id)
    elif send_type == 83:
        data = get_sent_candidates(db, campaign_id)

    return data


@mailing_routes.get("/mailing/send/campaign/camp/", tags=["Mailing"])
def get_inf_campaign_camp(
    camp_id: int,
    campers: bool,
    staffs: bool,
    school: bool,
    db: Session = Depends(get_db),
):
    """
    Significa traer la info necesaria para un correo que se enviará a
    participantes de un campamento
    """

    templates = get_all_massive_template(db)
    campers_info = []
    staffs_info = []
    school_info = None
    if campers:
        campers_complete = get_campers_for_camp(db, camp_id)
        for camper_c in campers_complete:
            campers_info.append(
                {
                    "camper_full_name": getattr(camper_c, "camper_full_name"),
                    "tutor_full_name": getattr(camper_c, "tutor_full_name"),
                    "tutor_email": getattr(camper_c, "tutor_email"),
                    "second_tutor_full_name": getattr(
                        camper_c, "second_tutor_full_name"
                    ),
                    "second_tutor_email": getattr(camper_c, "second_tutor_email"),
                }
            )
    if staffs:
        staffs_complete = get_staff_in_camp(db, camp_id)
        for staff_c in staffs_complete:
            staffs_info.append(
                {
                    "staff_full_name": getattr(staff_c, "staff_full_name"),
                    "staff_email": getattr(staff_c, "staff_email"),
                }
            )
    if school:
        school_info = {"school": "Escuela 1", "school_email": "escuela@correo.com"}

    return {
        "massive_templates": templates,
        "campers": campers_info,
        "staffs": staffs_info,
        "school": school_info,
    }


@mailing_routes.get("/mailing/send/campaign/camps/", tags=["Mailing"])
def get_inf_campaign_camps(
    camps_id: list[int],
    campers: bool,
    staffs: bool,
    school: bool,
    db: Session = Depends(get_db),
):
    """
    Significa traer la info necesaria para un correo que se enviará a diferentes
    participantes de varios campamento
    """

    templates = get_all_massive_template(db)
    campers_info = []
    staffs_info = []
    school_info = None
    if campers:
        campers_complete = get_campers_for_camp(db, camps_id[0])
        for camper_c in campers_complete:
            campers_info.append(
                {
                    "camper_full_name": getattr(camper_c, "camper_full_name"),
                    "tutor_full_name": getattr(camper_c, "tutor_full_name"),
                    "tutor_email": getattr(camper_c, "tutor_email"),
                    "second_tutor_full_name": getattr(
                        camper_c, "second_tutor_full_name"
                    ),
                    "second_tutor_email": getattr(camper_c, "second_tutor_email"),
                }
            )
    if staffs:
        staffs_complete = get_staff_in_camp(db, camps_id[0])
        for staff_c in staffs_complete:
            staffs_info.append(
                {
                    "staff_full_name": getattr(staff_c, "staff_full_name"),
                    "staff_email": getattr(staff_c, "staff_email"),
                }
            )
    if school:
        school_info = {"school": "Escuela 1", "school_email": "escuela@correo.com"}

    return {
        "massive_templates": templates,
        "campers": campers_info,
        "staffs": staffs_info,
        "school": school_info,
    }


@mailing_routes.get("/mailing/send/campaign/training/", tags=["Mailing"])
def get_inf_campaign_training(training_id: int, db: Session = Depends(get_db)):
    """
    Significa traer la info necesaria para un correo que se enviará a diferentes
    participantes de una capacitación
    """
    templates = get_all_massive_template(db)
    staffs_complete = get_all_staff_in_training_event(db, training_id)

    return {
        "massive_templates": templates,
        "staffs": staffs_complete,
    }


@mailing_routes.get("/mailing/send/campaign/candidates/", tags=["Mailing"])
def get_inf_campaign_candidates(season_id: int, db: Session = Depends(get_db)):
    """
    Significa traer la info necesaria para un correo que se enviará a diferentes
    candidatos a ser staff de una temporada
    """
    templates = get_all_massive_template(db)
    staffs_complete = get_all_prospect_by_season(db, season_id)

    return {
        "massive_templates": templates,
        "staffs": staffs_complete,
    }


@mailing_routes.post("/mailing/send/email/", tags=["Mailings"])
def send_massive_email(campaign_send: CampaignSend, db: Session = Depends(get_db)):

    return 1


