from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.catalogs.pathological_background_crud import (
    get_all_pathological_background,
    get_pathological_background_by_uuid,
    create_new_pathological_background,
    update_pathological_background_by_id,
    delete_pathological_back
)
from schema.catalogs.pathological_back_schema import(
    PathologicalBackgroundCreate,
    PathologicalBackgroundModify
)
from utils.db import SessionLocal

pathological_background_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@pathological_background_routes.get("/pathological_background/", tags=["Catalogs"])
def get_pathological_background(db: Session = Depends(get_db)):
    list_pathological_background = get_all_pathological_background(db)
    return {"data": list_pathological_background}


@pathological_background_routes.get("/pathological_background/{pathological_background_id}", tags=["Catalogs"])
def get_pathological_background_by_id(pathological_background_id:str,db: Session = Depends(get_db)):
    list_pathological_background = get_pathological_background_by_uuid(db,pathological_background_id)
    return {"data": list_pathological_background}


@pathological_background_routes.post("/pathological_background/", tags=["Catalogs"])
def create_pathological_background(new_prueba:PathologicalBackgroundCreate,db: Session = Depends(get_db)):
    list_pathological_background = create_new_pathological_background(db,new_prueba)
    return {"data": list_pathological_background}

@pathological_background_routes.post("/pathological_background/{pathological_background_id}", tags=["Catalogs"])
def update_pathological_background(pathological_background_id:str,modify_pathological_background:PathologicalBackgroundModify,db: Session = Depends(get_db)):

    update_data = modify_pathological_background.dict(exclude_unset=True)
    print(update_data)
    pathological_background_upcdate_result = update_pathological_background_by_id(db,pathological_background_id,update_data)

    if pathological_background_upcdate_result != 0:
        exist_pathological_background = get_pathological_background_by_uuid(db, pathological_background_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_pathological_background}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@pathological_background_routes.delete("/delete_pathological_back/{pathological_back_id}", tags=["Catalogs"])
def delete_pathological_back_by_id(pathological_back_id:int, db: Session = Depends(get_db)):
    response = delete_pathological_back(db, pathological_back_id)
    if response == None:
        raise HTTPException(status_code=404, detail="Pathological background not found")

    if response['status'] == 3:
        raise HTTPException(status_code=500, detail= response)
    return{ "detail": response } 

    
