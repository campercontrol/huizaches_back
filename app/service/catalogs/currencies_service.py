from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.catalogs.currencies_crud import (
    get_all_currencies,
    get_currencies_by_uuid,
    create_new_currencies,
    update_currencies_by_id
)
from schema.catalogs.currencies_schema import(
    CurrenciesCreate,
    CurrenciesModify
)
from utils.db import SessionLocal

currencies_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@currencies_routes.get("/currencies/", tags=["Catalogs"])
def get_currencies(db: Session = Depends(get_db)):
    list_currencies = get_all_currencies(db)
    return {"data": list_currencies}


@currencies_routes.get("/currencies/{currencies_id}", tags=["Catalogs"])
def get_currencies_by_id(currencies_id:str,db: Session = Depends(get_db)):
    list_currencies = get_currencies_by_uuid(db,currencies_id)
    return {"data": list_currencies}


@currencies_routes.post("/currencies/", tags=["Catalogs"])
def create_currencies(new_prueba:CurrenciesCreate,db: Session = Depends(get_db)):
    list_currencies = create_new_currencies(db,new_prueba)
    return {"data": list_currencies}

@currencies_routes.post("/currencies/{currencies_id}", tags=["Catalogs"])
def create_currencies(currencies_id:str,modify_currencies:CurrenciesModify,db: Session = Depends(get_db)):

    update_data = modify_currencies.dict(exclude_unset=True)
    print(update_data)
    currencies_upcdate_result = update_currencies_by_id(db,currencies_id,update_data)

    if currencies_upcdate_result != 0:
        exist_currencies = get_currencies_by_uuid(db, currencies_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_currencies}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

