from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.campers.parent_crud import (
    get_all_parent,
    get_parent_by_uuid,
    create_new_parent,
    update_parent_by_id,
)    

from schema.campers.parent_schema import(
    ParentCreate,
    ParentModify

)
from utils.db import SessionLocal

parent_routes = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@parent_routes.get("/parent/", tags=["Campers"])
def get_parent(db: Session = Depends(get_db)):
    list_parent = get_all_parent(db)
    return {"data": list_parent}

@parent_routes.get("/parent/{parent_id}", tags=["Campers"])
def get_parent_by_id(parent_id:str, db: Session = Depends(get_db)):
    list_parent = get_parent_by_uuid(db, parent_id)
    return {"data": list_parent}

@parent_routes.post("/parent/", tags=["Campers"])
def create_parent(new_parent:ParentCreate, db: Session =Depends(get_db)):
    list_parent = create_new_parent(db, new_parent)
    return {"data": list_parent}

@parent_routes.patch("/parent/{parent_id}", tags=["Campers"])
def update_parent(parent_id:str,modify_parent:ParentModify,db: Session = Depends(get_db)):

    update_data = modify_parent.dict(exclude_unset=True)
    print(update_data)
    parent_upcdate_result = update_parent_by_id(db,parent_id,update_data)

    if parent_upcdate_result != 0:
        exist_parent = get_parent_by_uuid(db, parent_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_parent}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}
    
