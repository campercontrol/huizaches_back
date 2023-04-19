from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.catalogs.pathological_background_family_crud import (
    get_all_pathological_background_family,
    get_pathological_background_family_by_uuid,
    create_new_pathological_background_family,
    update_pathological_background_family_by_id
)
from schema.catalogs.pathological_back_fm_schema import(
    PathologicalBackgroundFamilyCreate,
    PathologicalBackgroundFamilyModify
)
from utils.db import SessionLocal

pathological_background_family_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@pathological_background_family_routes.get("/pathological_background_family/", tags=["Catalogs"])
def get_pathological_background_family(db: Session = Depends(get_db)):
    list_pathological_background_family = get_all_pathological_background_family(db)
    return {"data": list_pathological_background_family}


@pathological_background_family_routes.get("/pathological_background_family/{pathological_background_family_id}", tags=["Catalogs"])
def get_pathological_background_family_by_id(pathological_background_family_id:str,db: Session = Depends(get_db)):
    list_pathological_background_family = get_pathological_background_family_by_uuid(db,pathological_background_family_id)
    return {"data": list_pathological_background_family}


@pathological_background_family_routes.post("/pathological_background_family/", tags=["Catalogs"])
def create_pathological_background_family(new_prueba:PathologicalBackgroundFamilyCreate,db: Session = Depends(get_db)):
    list_pathological_background_family = create_new_pathological_background_family(db,new_prueba)
    return {"data": list_pathological_background_family}

@pathological_background_family_routes.post("/pathological_background_family/{pathological_background_family_id}", tags=["Catalogs"])
def create_pathological_background_family(pathological_background_family_id:str,modify_pathological_background_family:PathologicalBackgroundFamilyModify,db: Session = Depends(get_db)):

    update_data = modify_pathological_background_family.dict(exclude_unset=True)
    print(update_data)
    pathological_background_family_upcdate_result = update_pathological_background_family_by_id(db,pathological_background_family_id,update_data)

    if pathological_background_family_upcdate_result != 0:
        exist_pathological_background_family = get_pathological_background_family_by_uuid(db, pathological_background_family_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_pathological_background_family}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

