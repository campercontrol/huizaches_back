from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.catalogs.vaccine_crud import (
    get_all_vaccine,
    get_vaccine_by_uuid,
    create_new_vaccine,
    update_vaccine_by_id
)
from schema.catalogs.vaccine_schema import(
    VaccineCreate,
    VaccineModify
)
from utils.db import SessionLocal

vaccine_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@vaccine_routes.get("/vaccine/", tags=["Catalogs"])
def get_vaccine(db: Session = Depends(get_db)):
    list_vaccine = get_all_vaccine(db)
    return {"data": list_vaccine}


@vaccine_routes.get("/vaccine/{vaccine_id}", tags=["Catalogs"])
def get_vaccine_by_id(vaccine_id:str,db: Session = Depends(get_db)):
    list_vaccine = get_vaccine_by_uuid(db,vaccine_id)
    return {"data": list_vaccine}


@vaccine_routes.post("/vaccine/", tags=["Catalogs"])
def create_vaccine(new_prueba:VaccineCreate,db: Session = Depends(get_db)):
    list_vaccine = create_new_vaccine(db,new_prueba)
    return {"data": list_vaccine}

@vaccine_routes.post("/vaccine/{vaccine_id}", tags=["Catalogs"])
def create_vaccine(vaccine_id:str,modify_vaccine:VaccineModify,db: Session = Depends(get_db)):

    update_data = modify_vaccine.dict(exclude_unset=True)
    print(update_data)
    vaccine_upcdate_result = update_vaccine_by_id(db,vaccine_id,update_data)

    if vaccine_upcdate_result != 0:
        exist_vaccine = get_vaccine_by_uuid(db, vaccine_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_vaccine}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

