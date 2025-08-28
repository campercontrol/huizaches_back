from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.crud_prueba import (
    get_all_prueba,
    get_prueba_by_uuid,
    create_new_prueba,
    update_prueba_by_id
)
from schema.prueba_schema import(
    PruebaCreate,
    PruebaModify
)
from utils.db import SessionLocal

from model.user import User

prueba_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@prueba_routes.get("/prueba_autenticacion/", tags=["Demo"])
def get_prueba(
        ):
    return {"data": "Autenticacion Correcta"}


@prueba_routes.get("/prueba/{prueba_id}", tags=["Demo"])
def get_prueba_by_id(
    prueba_id:str,
    db: Session = Depends(get_db)
        ):
    list_prueba = get_prueba_by_uuid(db,prueba_id)
    return {"data": list_prueba}


@prueba_routes.post("/prueba/", tags=["Demo"])
def create_prueba(
    new_prueba:PruebaCreate,
    db: Session = Depends(get_db)
        ):
    list_prueba = create_new_prueba(db,new_prueba)
    return {"data": list_prueba}

@prueba_routes.post("/prueba/{prueba_id}", tags=["Demo"])
def create_prueba(
    prueba_id:str,
    modify_prueba:PruebaModify,
    db: Session = Depends(get_db)
        ):

    update_data = modify_prueba.dict(exclude_unset=True)
    print(update_data)
    prueba_upcdate_result = update_prueba_by_id(db,prueba_id,update_data)

    if prueba_upcdate_result != 0:
        exist_prueba = get_prueba_by_uuid(db, prueba_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_prueba}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

