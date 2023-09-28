from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.mailings.email_template_crud import (
    get_all_email_template,
    get_all_system_template
)
from crud.mailings.campaign_crud import (
    get_all_campaign
)

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
    list_template = get_all_email_template(db)
    return {"data": list_template}

@mailing_routes.get("/mailing/template/system/", tags=["Mailing"])
def get_email_template_system(db: Session = Depends(get_db)):
    list_template = get_all_system_template(db)
    return {"data": list_template}

@mailing_routes.get("/mailing/campaign/", tags=["Mailing"])
def get_campaign(db: Session = Depends(get_db)):
    list_campaign = get_all_campaign(db)
    return {"data": list_campaign}