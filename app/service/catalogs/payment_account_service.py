from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.catalogs.payment_account_crud import (
    get_all_payment_account,
    get_payment_account_by_uuid,
    create_new_payment_account,
    update_payment_account_by_id,
    delete_payment_account
)
from schema.catalogs.payment_account_schema import(
    PaymentAccountCreate,
    PaymentAccountModify
)
from utils.db import SessionLocal

payment_account_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@payment_account_routes.get("/payment_account/", tags=["Catalogs"])
def get_payment_account(db: Session = Depends(get_db)):
    list_payment_account = get_all_payment_account(db)
    return {"data": list_payment_account}


@payment_account_routes.get("/payment_account/{payment_account_id}", tags=["Catalogs"])
def get_payment_account_by_id(payment_account_id:str,db: Session = Depends(get_db)):
    list_payment_account = get_payment_account_by_uuid(db,payment_account_id)
    return {"data": list_payment_account}


@payment_account_routes.post("/payment_account/", tags=["Catalogs"])
def create_payment_account(new_prueba:PaymentAccountCreate,db: Session = Depends(get_db)):
    list_payment_account = create_new_payment_account(db,new_prueba)
    return {"data": list_payment_account}

@payment_account_routes.post("/payment_account/{payment_account_id}", tags=["Catalogs"])
def update_payment_account(payment_account_id:str,modify_payment_account:PaymentAccountModify,db: Session = Depends(get_db)):

    update_data = modify_payment_account.dict(exclude_unset=True)
    print(update_data)
    payment_account_upcdate_result = update_payment_account_by_id(db,payment_account_id,update_data)

    if payment_account_upcdate_result != 0:
        exist_payment_account = get_payment_account_by_uuid(db, payment_account_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_payment_account}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@payment_account_routes.delete("/delete_payment_account/{payment_account_id}", tags=["Catalogs"])
def delete_payment_account_by_id(payment_account_id:int, db: Session = Depends(get_db)):
    status = delete_payment_account(db, payment_account_id)
    return{"status": status}