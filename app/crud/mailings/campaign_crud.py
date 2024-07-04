from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import func
from model.mailings import Campaign, CamperCampaign, EmailTemplate
from model.camps import Camp
from model.campers import Camper
from schema.mailings.campaign_schema import CampaignCreate, CampaignModify
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_campaign(db):
    rows = db.query(Campaign).all()
    return rows

def get_campaign_by_uuid(db, campaign_id):
    return (
        db.query(Campaign)
        .filter_by(
            id=campaign_id,
        )
        .first()
    )

def get_campaign_all_info_by_id(db, campaign_id):
    campaign_query = db.query(Campaign.id, EmailTemplate.template, EmailTemplate.title).join(EmailTemplate, EmailTemplate.id == Campaign.template_id).filter(Campaign.id == campaign_id)
    campaign_campers_query = db.query(Camper.id, func.concat(Camper.name, ' ', Camper.lastname_father, ' ', Camper.lastname_mother).label('camper_name')).join(CamperCampaign, CamperCampaign.camper_id == Camper.id).filter(CamperCampaign.campaign_id == campaign_id)
    campaign_camp_query = db.query(Camp.id, Camp.name).join(CamperCampaign, CamperCampaign.camp_id == Camp.id).filter(CamperCampaign.campaign_id == campaign_id).distinct()
    
    campaign_campers = db.execute(campaign_campers_query)
    campaign = db.execute(campaign_query)
    campaign_camp = db.execute(campaign_camp_query)

    campaign = campaign.mappings().first()
    campaign_campers = campaign_campers.mappings().all()
    campaign_camp = campaign_camp.mappings().all()
    
    campaign_all_info = {
        "campaign": campaign,
        "campers": campaign_campers,
        "camps": campaign_camp
    }
    return campaign_all_info

def create_campaign(db, new_campaign):
    new_campaign = Campaign(**new_campaign)
    try:
        db.add(new_campaign)
        db.commit()
        db.refresh(new_campaign)
        return new_campaign
    except SQLAlchemyError as e:
        print(e)
        return None  
    
def add_camper_to_campaign(db, camper_campaign):
    new_campaign = CamperCampaign(**camper_campaign)
    try:
        db.add(new_campaign)
        db.commit()
        db.refresh(new_campaign)
        return new_campaign
    except SQLAlchemyError as e:
        print(e)
        return None  

def create_new_campaign(db, new_campaign: CampaignCreate):
    db_campaign = None
    try:
        db_campaign = Campaign(**new_campaign.dict())
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_campaign = None
        return db_campaign
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_campaign


def update_campaign_by_id(db, campaign_id, modify_campaign: CampaignModify):
    rows_updated = (
        db.query(Campaign).filter_by(id=campaign_id).update(modify_campaign, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def delete_campaign(db: Session, campaign_id:int):
    campaign = db.query(Campaign).filter(Campaign.id==campaign_id).first()
    db.delete(campaign)
    db.commit()
    return {"status" : True}