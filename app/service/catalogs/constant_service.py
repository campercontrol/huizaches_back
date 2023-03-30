from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.catalogs.constant_crud import (
    get_all_constant,
    get_constant_by_uuid,
    create_new_constant,
    update_constant_by_id
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

@constant_routes.post("/constant/{constant_id}", tags=["Constants"])
def create_constant(constant_id:str,modify_constant:ConstantModify,db: Session = Depends(get_db)):

    update_data = modify_constant.dict(exclude_unset=True)
    print(update_data)
    constant_upcdate_result = update_constant_by_id(db,constant_id,update_data)

    if constant_upcdate_result != 0:
        exist_constant = get_constant_by_uuid(db, constant_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_constant}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

