from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.mailings.email_template_crud import (
    get_all_email_template,
    get_email_template_by_uuid,
    create_new_email_template,
    update_email_template_by_id,
    delete_email_template
)
from crud.catalogs.constant_crud import (
    get_all_email_template
)
from schema.mailings.email_template_schema import(
    EmailTemplateCreate,
    EmailTemplateModify
)
from utils.db import SessionLocal

email_template_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@email_template_routes.get("/email_template/", tags=["Mailing"])
def get_email_template(db: Session = Depends(get_db)):
    list_email_template = get_all_email_template(db)
    return {"data": list_email_template}


@email_template_routes.get("/email/massive/template/{email_template_id}", tags=["Mailing"])
def get_massive_template_by_id(email_template_id:str,db: Session = Depends(get_db)):
    list_email_template = get_email_template_by_uuid(db,email_template_id)
    return {"data": list_email_template}

@email_template_routes.get("/email/system/template/{email_template_id}", tags=["Mailing"])
def get_system_template_by_id(email_template_id:str,db: Session = Depends(get_db)):
    list_email_type = get_all_email_template(db, "es")
    templates = get_email_template_by_uuid(db,email_template_id)
    return {
        "template_type": list_email_type,
        "template": templates
        }

@email_template_routes.post("/email/template/", tags=["Mailing"])
def create_email_template(new_prueba:EmailTemplateCreate,db: Session = Depends(get_db)):
    list_email_template = create_new_email_template(db,new_prueba)
    return {"data": list_email_template}

@email_template_routes.patch("/email/template/{email_template_id}", tags=["Mailing"])
def modify_email_template(email_template_id:str,modify_email_template:EmailTemplateModify,db: Session = Depends(get_db)):

    update_data = modify_email_template.dict(exclude_unset=True)
    print(update_data)
    email_template_upcdate_result = update_email_template_by_id(db,email_template_id,update_data)

    if email_template_upcdate_result != 0:
        exist_email_template = get_email_template_by_uuid(db, email_template_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_email_template}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@email_template_routes.delete("/delete_email_template/{email_template_id}", tags=["Mailing"])
def delete_email_template_by_id(email_template_id:int, db: Session = Depends(get_db)):
    status = delete_email_template(db, email_template_id)
    return{"status": status}