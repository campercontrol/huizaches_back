from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from model.mailings import Campaign
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