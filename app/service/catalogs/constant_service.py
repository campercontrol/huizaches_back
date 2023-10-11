from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.catalogs.constant_crud import (
    get_all_constant,
    get_constant_by_uuid,
    create_new_constant,
    update_constant_by_id,
    get_all_answer,
    get_all_assign_choice,
    get_all_blood_type,
    get_all_camp_status,
    get_all_gender,
    get_all_grade,
    get_all_med_auth,
    get_all_rol_colors,
    get_all_triage,
    get_all_user_group,
    get_all_email_template_type,
    get_all_email_send_type
)
from schema.catalogs.constant_schema import(
    ConstantCreate,
    ConstantModify
)
from utils.db import SessionLocal

constant_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@constant_routes.get("/constant/", tags=["Constants"])
def get_constant(db: Session = Depends(get_db)):
    list_constant = get_all_constant(db)
    return {"data": list_constant}


@constant_routes.get("/constant/{constant_id}", tags=["Constants"])
def get_constant_by_id(constant_id:str,db: Session = Depends(get_db)):
    list_constant = get_constant_by_uuid(db,constant_id)
    return {"data": list_constant}


@constant_routes.post("/constant/", tags=["Constants"])
def create_constant(new_constant:ConstantCreate,db: Session = Depends(get_db)):
    list_constant = create_new_constant(db,new_constant)
    return {"data": list_constant}

@constant_routes.patch("/constant/{constant_id}", tags=["Constants"])
def modify_constant(constant_id:str,modify_constant:ConstantModify,db: Session = Depends(get_db)):

    update_data = modify_constant.dict(exclude_unset=True)
    constant_upcdate_result = update_constant_by_id(db,constant_id,update_data)

    if constant_upcdate_result != 0:
        exist_constant = get_constant_by_uuid(db, constant_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_constant}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}


@constant_routes.get("/get_all_answer/{language}", tags=["Constants"])
def get_answer(language:str, db: Session=Depends(get_db)):
    list_constant= get_all_answer(db, language)
    return {"data": list_constant} 

@constant_routes.get("/get_all_assign_chioce/{language}", tags=["Constants"])
def get_assign_chioce(language:str, db: Session=Depends(get_db)):
    list_constant= get_all_assign_choice(db, language)
    return {"data": list_constant} 

@constant_routes.get("/get_all_blood_type/{language}", tags=["Constants"])
def get_blood_type(language:str, db: Session=Depends(get_db)):
    list_constant= get_all_blood_type(db, language)
    return {"data": list_constant} 

@constant_routes.get("/get_all_camp_status/{language}", tags=["Constants"])
def get_camp_status(language:str, db: Session=Depends(get_db)):
    list_constant= get_all_camp_status(db, language)
    return {"data": list_constant} 

@constant_routes.get("/get_all_gender/{language}", tags=["Constants"])
def get_gender(language:str, db: Session=Depends(get_db)):
    list_constant= get_all_gender(db, language)
    return {"data": list_constant} 

@constant_routes.get("/get_all_grade/{language}", tags=["Constants"])
def get_grade(language:str, db: Session=Depends(get_db)):
    list_constant= get_all_grade(db, language)
    return {"data": list_constant} 

@constant_routes.get("/get_all_med_auth/{language}", tags=["Constants"])
def get_med_auth(language:str, db: Session=Depends(get_db)):
    list_constant= get_all_med_auth(db, language)
    return {"data": list_constant} 

@constant_routes.get("/get_all_rol_colors/{language}", tags=["Constants"])
def get_rol_colors(language:str, db: Session=Depends(get_db)):
    list_constant= get_all_rol_colors(db, language)
    return {"data": list_constant} 

@constant_routes.get("/get_all_triage/{language}", tags=["Constants"])
def get_triage(language:str, db: Session=Depends(get_db)):
    list_constant= get_all_triage(db, language)
    return {"data": list_constant} 

@constant_routes.get("/get_all_user_group/{language}", tags=["Constants"])
def get_user_group(language:str, db: Session=Depends(get_db)):
    list_constant= get_all_user_group(db, language)
    return {"data": list_constant} 

@constant_routes.get("/get/mailing/template/{language}", tags=["Constants"])
def get_email_template(language:str ="es", db: Session=Depends(get_db)):
    list_constant= get_all_email_template_type(db, language)
    return {"data": list_constant} 

@constant_routes.get("/get/mailing/type/{language}", tags=["Constants"])
def get_email_type(language:str ="es", db: Session=Depends(get_db)):
    list_constant= get_all_email_send_type(db, language)
    return {"data": list_constant} 
