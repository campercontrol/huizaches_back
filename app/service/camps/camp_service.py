from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.camps.camp_crud import (
    get_all_camp,
    get_all_active_camp,
    get_camp_for_camper,
    get_camp_by_id,
    create_new_camp,
    update_camp_by_id   
)
from crud.camps.camper_in_camp_crud import (
    create_new_camper_in_camp,
    get_all_camper_in_camp
)
from schema.camps.camp_schema import(
    CampCreate,
    CampModify
)
from schema.camps.camper_in_camp_schema import (
    CamperInCampCreate,
    CamperInCampModify
)
from utils.db import SessionLocal

camp_router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@camp_router.get("/camp/", tags=["Camps"])
def get_camp(db: Session = Depends(get_db)):
    list_camp = get_all_camp(db)
    return {"data": list_camp}

@camp_router.get("/active_camp/", tags=["Camps"])
def get__active_camp(db: Session = Depends(get_db)):
    list_camp = get_all_active_camp(db)
    return {"data": list_camp}

@camp_router.get("/get_camps_for_camper/{camper_id}/{school_id}", tags=["Camps"])
def get_camps_for_camper(camper_id:int, school_id:int, db: Session = Depends(get_db)):
    list_camp = get_camp_for_camper(db, camper_id, school_id)
    return {"data": list_camp}

@camp_router.get("/camp/{camp_id}", tags=["Camps"])
def get_camp_id(camp_id:int,db: Session = Depends(get_db)):
    camp = get_camp_by_id(db,camp_id)
    return {"data": camp}


@camp_router.post("/camp/", tags=["Camps"])
def create_camp(new_camp:CampCreate,db: Session = Depends(get_db)):
    camp = create_new_camp(db,new_camp)
    return {"data": camp}

@camp_router.patch("/camp/{camp_id}", tags=["Camps"])
def update_camp(camp_id:int, modify_camp:CampModify, db: Session = Depends(get_db)):

    update_data = modify_camp.dict(exclude_unset=True)
    camp_update_result = update_camp_by_id(db,camp_id,update_data)

    if camp_update_result != 0:
        exist_camp = get_camp_by_id(db, camp_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_camp}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@camp_router.post("/subscribe_camp/", tags=["Camps"])
def subscribe_camp(new_camper_in_camp:CamperInCampCreate, db: Session = Depends(get_db)):
    camper_in_camp = create_new_camper_in_camp(db, new_camper_in_camp)
    return {"data": camper_in_camp}

@camp_router.get("/camperincamp/", tags=["Camps"])
def get_camperincamp(db: Session = Depends(get_db)):
    list_camp = get_all_camper_in_camp(db)
    return {"data": list_camp}
