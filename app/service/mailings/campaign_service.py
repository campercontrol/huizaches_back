from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.mailings.campaign_crud import (
    get_all_campaign,
    get_campaign_by_uuid,
    create_new_campaign,
    update_campaign_by_id,
    delete_campaign
)
from schema.mailings.campaign_schema import(
    CampaignCreate,
    CampaignModify
)
from utils.db import SessionLocal

campaign_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@campaign_routes.get("/campaign/", tags=["Mailing"])
def get_campaign(db: Session = Depends(get_db)):
    list_campaign = get_all_campaign(db)
    return {"data": list_campaign}


@campaign_routes.get("/campaign/{campaign_id}", tags=["Mailing"])
def get_campaign_by_id(campaign_id:str,db: Session = Depends(get_db)):
    list_campaign = get_campaign_by_uuid(db,campaign_id)
    return {"data": list_campaign}


@campaign_routes.post("/campaign/", tags=["Mailing"])
def create_campaign(new_prueba:CampaignCreate,db: Session = Depends(get_db)):
    list_campaign = create_new_campaign(db,new_prueba)
    return {"data": list_campaign}

@campaign_routes.patch("/campaign/{campaign_id}", tags=["Mailing"])
def modify_campaign(campaign_id:str,modify_campaign:CampaignModify,db: Session = Depends(get_db)):

    update_data = modify_campaign.dict(exclude_unset=True)
    print(update_data)
    campaign_upcdate_result = update_campaign_by_id(db,campaign_id,update_data)

    if campaign_upcdate_result != 0:
        exist_campaign = get_campaign_by_uuid(db, campaign_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_campaign}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@campaign_routes.delete("/delete_campaign/{campaign_id}", tags=["Mailing"])
def delete_campaign_by_id(campaign_id:int, db: Session = Depends(get_db)):
    status = delete_campaign(db, campaign_id)
    return{"status": status}