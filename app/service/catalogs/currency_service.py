from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.catalogs.currency_crud import (
    get_all_currency,
    get_currency_by_uuid,
    create_new_currency,
    update_currency_by_id,
    delete_currency
)
from schema.catalogs.currency_schema import(
    CurrencyCreate,
    CurrencyModify
)
from utils.db import SessionLocal

currency_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@currency_routes.get("/currency/", tags=["Catalogs"])
def get_currency(db: Session = Depends(get_db)):
    list_currency = get_all_currency(db)
    return {"data": list_currency}


@currency_routes.get("/currency/{currency_id}", tags=["Catalogs"])
def get_currency_by_id(currency_id:str,db: Session = Depends(get_db)):
    list_currency = get_currency_by_uuid(db,currency_id)
    return {"data": list_currency}


@currency_routes.post("/currency/", tags=["Catalogs"])
def create_currency(new_prueba:CurrencyCreate,db: Session = Depends(get_db)):
    list_currency = create_new_currency(db,new_prueba)
    return {"data": list_currency}

@currency_routes.patch("/currency/{currency_id}", tags=["Catalogs"])
def modify_currency(currency_id:str,modify_currency:CurrencyModify,db: Session = Depends(get_db)):

    update_data = modify_currency.dict(exclude_unset=True)
    print(update_data)
    currency_upcdate_result = update_currency_by_id(db,currency_id,update_data)

    if currency_upcdate_result != 0:
        exist_currency = get_currency_by_uuid(db, currency_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_currency}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@currency_routes.delete("/delete_currency/{currency_id}", tags=["Catalogs"])
def delete_currency_by_id(currency_id:int, db: Session = Depends(get_db)):
    response = delete_currency(db, currency_id)

    if response['status'] == 3:
        raise HTTPException(status_code=500, detail= response['detail'])
    return response
