from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.payments.payment_transaction_type_crud import (
    get_all_payment_transaction_type,
    get_payment_transaction_type_by_id,
    update_payment_transaction_type_by_id,
    create_new_payment_transaction_type,
    
)
from schema.payments.payment_transaction_type_schema import(
    PaymentTransactionTypeCreate,
    PaymentTransactionTypeModify
)
from utils.db import SessionLocal

payment_transaction_type_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@payment_transaction_type_routes.get("/payment_transaction_type/", tags=["Payments"])
def get_payment_transaction_type(db: Session = Depends(get_db)):
    list_payment_transaction_type = get_all_payment_transaction_type(db)
    return {"data": list_payment_transaction_type}

@payment_transaction_type_routes.get("/payment_transaction_type/{payment_transaction_type_id}", tags=["Payments"])
def get_payment_transaction_type_by__id(payment_transaction_type_id:str,db: Session = Depends(get_db)):
    payment = get_payment_transaction_type_by_id(db,payment_transaction_type_id)
    return {"data": payment}

@payment_transaction_type_routes.post("/payment_transaction_type/", tags=["Payments"])
def create_payment_transaction_type(new_payment_transaction_type:PaymentTransactionTypeCreate,db: Session = Depends(get_db)):
    payment = create_new_payment_transaction_type(db, new_payment_transaction_type)
    return {"data": payment}

@payment_transaction_type_routes.patch("/payment_transaction_type/{payment_transaction_type_id}", tags=["Payments"])
def update_payment_transaction_type(payment_transaction_type_id:str,modify_payment_transaction_type:PaymentTransactionTypeModify,db: Session = Depends(get_db)):

    update_data = modify_payment_transaction_type.dict(exclude_unset=True)
    print(update_data)
    payment_update_result = update_payment_transaction_type_by_id(db,payment_transaction_type_id,update_data)

    if payment_update_result != 0:
        exist_payment_transaction_type = get_payment_transaction_type_by_id(db, payment_transaction_type_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_payment_transaction_type}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

