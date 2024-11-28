from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.mailings.email_template_crud import (
    get_all_massive_template,
    get_all_system_template,
)
from crud.mailings.campaign_crud import get_all_campaign, create_new_campaign, add_camper_to_campaign
from crud.mailings.mailing_crud import (
    get_sent_camp,
    get_sent_camps,
    get_sent_training,
    get_sent_candidates,
)
from crud.camps.camper_in_camp_crud import get_campers_for_camp, get_campers_in_camp_mailing
from crud.camps.staff_in_camp_crud import get_staff_in_camp
from crud.training.staff_in_training_crud import get_all_staff_in_training_event
from crud.staffs.staff_crud import get_all_prospect_by_season
from crud.campers.parent_crud import get_parent_by_camper_id
from crud.campers.camper_crud import get_camper_info_mailing
from crud.camps.camp_crud import get_school_info_by_camp, get_camp_info_by_id_mailing
from crud.staffs.staff_crud import get_staff_info_mailing
from crud.mailings.campaign_crud import get_campaign_all_info_by_id
from crud.training.training_crud import get_training_by_id
from model.mailings import (
    Campaign
)
from model.camps import Camp
from schema.mailings.campaign_schema import CampaignSend, CampaignSendStaff

from helper.mailing_helpers import send_mail_template, send_mail_template_plain_text
from utils.email_tools import send_simple_message

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
    school_info = []
    if campers:
        campers_complete = get_campers_for_camp(db, camp_id)
        print("CAMPERS!!!!!!!!!!!!!")
        print(campers_complete)
        for camper_c in campers_complete:
            campers_info.append(
                {   
                    "camper_id": camper_c["camper_id"],
                    "camper_full_name": camper_c["camper_full_name"],
                    "tutor_full_name": camper_c["tutor_full_name"],
                    "tutor_email": camper_c["tutor_full_name"],
                    "second_tutor_full_name": camper_c["second_tutor_full_name"],
                    "second_tutor_email": camper_c["second_tutor_email"]
                }
            )
    if staffs:
        staffs_complete = get_staff_in_camp(db, camp_id)
        for staff_c in staffs_complete:
            staffs_info.append(
                {
                    "staff_id": staff_c["staff_id"],
                    "staff_full_name": staff_c["staff_full_name"],
                    "staff_email": staff_c["staff_email"]
                }
            )
    if school:
        school_info = {"school_id": 1, "school": "Escuela 1", "school_email": "escuela@correo.com"}

    return {
        "massive_templates": templates,
        "campers": campers_info,
        "staffs": staffs_info,
        "school": school_info,
    }


@mailing_routes.post("/mailing/send/campaign/camps/", tags=["Mailing"])
def get_inf_campaign_camps(
    camps_id: "list[int]",
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
    
    if len(camps_id) > 0:
        camps = []
        campers_list = []
        staff_list = []
        school_list = {}
        mailing_campaign = {}
        for camp_id in camps_id:
            if campers: 
                campers_list = get_campers_in_camp_mailing(db, camp_id)
            if staffs:
                staff_list =  get_staff_in_camp(db, camp_id)
            if school:
                school_list = get_school_info_by_camp(db, camp_id)         
            camp_info_query = db.query(Camp.id, Camp.name).filter(Camp.id == camp_id)
            
            camp_data = db.execute(camp_info_query)
            camp_info = camp_data.mappings().first()
            camps.append({"camp": {
                "name": camp_info.name,
                "id" : camp_info.id,
                "campers": campers_list,
                "staff": staff_list,
                "school": school_list
            }})
            
        mailing_campaign['massive_templates'] = templates
        mailing_campaign['camps'] = camps
        return mailing_campaign
    

@mailing_routes.get("/mailing/send/campaign/training/", tags=["Mailing"])
def get_inf_campaign_training(training_id: int, db: Session = Depends(get_db)):
    """
    Significa traer la info necesaria para un correo que se enviará a diferentes
    participantes de una capacitación
    """
    # templates = get_all_massive_template(db)
    # staffs_complete = get_all_staff_in_training_event(db, training_id)
    training_info = get_training_by_id(db, training_id)
    print(training_info)

    return 1
    # return {
    #     "massive_templates": templates,
    #     "staffs": staffs_complete,
    # }


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

@mailing_routes.get("/mailing/campaign_info/{campaign_id}", tags=["Mailing"])
def get_campaign_info(campaign_id: int, db: Session = Depends(get_db)):
    """
    Devuelve toda la información sobre un template enviado
    """
    campaign_info = get_campaign_all_info_by_id(db, campaign_id)
    
    if campaign_info["campaign"] == None:
         raise HTTPException(status_code=404)
    return campaign_info
@mailing_routes.post("/mailing/send/email/", tags=["Mailings"])
def send_massive_email(campaign_send: CampaignSend, db: Session = Depends(get_db)):
    camps = campaign_send.camps
    campaign = campaign_send.campaign
    template_id = campaign_send.campaign.template_id
    template_subject = campaign_send.email_subject
    template_body = campaign_send.template_body
    
    default_camper_variables = {
        "name": "",
        "fullname": "",
        "grade": "",
        "school": ""
    }
    default_payment_variables = {
        "payment_date": "",
        "payment_method": "",
        "txn_type": "",
        "txn_number": "",
    }
    new_campaign = create_new_campaign(db, campaign)

    if new_campaign == None:
        raise HTTPException(status_code=500, detail={"status": 3, "msg": "An error ocurred while creating the campaing"})
    
    for camp in camps:
        # print(camp["camp"]["id"])
        camp_info = get_camp_info_by_id_mailing(db, camp["camp"]["id"])
        campers = camp["camp"]["campers"]
        staffs = camp["camp"]["staff"]
        school = camp["camp"]["school"]
        if len(campers) > 0:
            for camper in campers:
                parent_info = get_parent_by_camper_id(db, camper["id"])
                camper_info = get_camper_info_mailing(db, camper["id"])
                email_context = {
                    "camper": camper_info,
                    "user": parent_info,
                    "camp": camp_info,
                    "payment": default_payment_variables
                                
                }
                camper_campaign = {
                    "campaign_id": new_campaign.id,
                    "camp_id": camp_info["id"],
                    "camper_id": camper["id"]
                }                
                sendmail_status = send_mail_template_plain_text(db, camper["tutor_email"], template_body, template_subject, email_context)
                if sendmail_status: 
                    add_camper_to_campaign(db, camper_campaign)
                
        if len(staffs) > 0: 
            for staff in staffs:
                staff_info = get_staff_info_mailing(db, staff["staff_id"])
                email_context = {
                    "camper": default_camper_variables,
                    "user": staff_info,
                    "camp": camp_info,
                    "payment": default_payment_variables
                }
                send_mail_template_plain_text(db, staff["staff_email"], template_body, template_subject, email_context)
        if school:        
            email_context = {
                "camper": default_camper_variables,
                "user": {
                    "name": school["name"],
                    "email": school["email"],
                },
                "payment": default_payment_variables,
                "camp": camp_info
            }
            send_mail_template_plain_text(db, school["email"], template_body, template_subject, email_context)
        
    return {"status": 1, "msg": "emails sent successfully"}


@mailing_routes.post("/mailing/send/email/staff_in_training", tags=["Mailings"])
def send_massive_email_staff_in_training(campaign_send: CampaignSendStaff, db: Session = Depends(get_db)):
    template_id = campaign_send.campaign.template_id
    staffs = campaign_send.staffs
    default_camper_variables = {
        "name": "",
        "fullname": "",
        "grade": "",
        "school": ""
    }
    default_payment_variables = {
        "payment_date": "",
        "payment_method": "",
        "txn_type": "",
        "txn_number": "",
    }
    default_camp_info_variables = {
        "name": "",
        "start": "",
        "end": "",
        "start_registration": "", 
        "end_registration": "",
        "registration": "",
        "url": "",
        "special_message": "",
        "special_message": "",
        "special_message_admin": "",
        "public_price": "",
        "insurance": "",
        "venue": "",
        "photo_url": "",
        "photo_password": "",
        "medical_report": "",
        "occupancy_camp": "",
        "school": "", 
        "location": ""
    }
    for staff in staffs:
        staff_info = get_staff_info_mailing(db, staff["id"])
        email_context = {
            "camper": default_camper_variables,
            "user": staff_info,
            "camp": default_camp_info_variables,
            "payment": default_payment_variables
        }
        send_mail_template(db, staff["email"],template_id, email_context)
            
    return {"status": 1, "msg": "emails sent successfully"}

