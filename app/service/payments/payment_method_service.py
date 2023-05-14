from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.payments.payment_method_crud import (
    get_all_payment_method,
    get_payment_method_by_id,
    update_payment_method_by_id,
    create_new_payment_method,
    
)
from schema.payments.payment_method_schema import(
    PaymentMethodCreate,
    PaymentMethodModify
)
from utils.db import SessionLocal

payment_method_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@payment_method_routes.get("/payment_method/", tags=["Payments"])
def get_payment_method(db: Session = Depends(get_db)):
    list_payment_method = get_all_payment_method(db)
    return {"data": list_payment_method}

@payment_method_routes.get("/payment_method/{payment_id}", tags=["Payments"])
def get_payment_method_by__id(payment_id:str,db: Session = Depends(get_db)):
    payment = get_payment_method_by_id(db,payment_id)
    return {"data": payment}

@payment_method_routes.post("/payment_method/", tags=["Payments"])
def create_payment_method(new_payment_method:PaymentMethodCreate,db: Session = Depends(get_db)):
    payment = create_new_payment_method(db, new_payment_method)
    return {"data": payment}

@payment_method_routes.patch("/payment_method/{payment_id}", tags=["Payments"])
def update_payment_method(payment_id:str,modify_payment_method:PaymentMethodModify,db: Session = Depends(get_db)):

    update_data = modify_payment_method.dict(exclude_unset=True)
    print(update_data)
    payment_update_result = update_payment_method_by_id(db,payment_id,update_data)

    if payment_update_result != 0:
        exist_payment_method = get_payment_method_by_id(db, payment_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_payment_method}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

