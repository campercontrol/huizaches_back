from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.camps.location_crud import (
    get_all_location,
    get_all_active_location_id_name,
    get_location_by_uuid,
    update_location_by_id,
    create_new_location
)
from schema.camps.location_schema import(
    LocationCreate,
    LocationModify
)
from utils.db import SessionLocal

location_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@location_routes.get("/location/", tags=["Camps"])
def get_location(db: Session = Depends(get_db)):
    list_location = get_all_location(db)
    return {"data": list_location}


@location_routes.get("/location/{location_id}", tags=["Camps"])
def get_location_by_id(location_id:str,db: Session = Depends(get_db)):
    location = get_location_by_uuid(db,location_id)
    return {"data": location}


@location_routes.post("/location/", tags=["Camps"])
def create_location(new_location:LocationCreate,db: Session = Depends(get_db)):
    location = create_new_location(db,new_location)
    return {"data": location}

@location_routes.patch("/location/{location_id}", tags=["Camps"])
def update_location(location_id:str, modify_location:LocationModify, db: Session = Depends(get_db)):

    update_data = modify_location.dict(exclude_unset=True)
    print(update_data)
    location_update_result = update_location_by_id(db,location_id,update_data)

    if location_update_result != 0:
        exist_location = get_location_by_uuid(db, location_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_location}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@location_routes.get("/active_location/", tags=["Camps"])
def get_all_active_location(db: Session = Depends(get_db)):
    list_location = get_all_active_location_id_name(db)
    return {"data": list_location}
