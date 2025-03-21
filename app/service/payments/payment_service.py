from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.payments.payment_crud import (
    get_all_payment,
    get_payment_by_id,
    update_payment_by_id,
    get_payment_by_camper_camp,
    get_payment_page_camper_in_camp,
    create_payment_controller,
    update_payment_controller
)
from schema.payments.payment_schema import(
    PaymentCreate,
    PaymentModify
)
from utils.db import SessionLocal

payment_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@payment_routes.get("/payment/", tags=["Payments"])
def get_payment(db: Session = Depends(get_db)):
    list_payment = get_all_payment(db)
    return {"data": list_payment}

@payment_routes.get("/payment/{payment_id}", tags=["Payments"])
def get_payment_by__id(payment_id:str,db: Session = Depends(get_db)):
    payment = get_payment_by_id(db,payment_id)
    return {"data": payment}

@payment_routes.post("/payment/", tags=["Payments"])
def post_payment(new_payment:PaymentCreate,db: Session = Depends(get_db)):
    
    result = create_payment_controller(db, new_payment)
    if result == 1:
        return {"detail": {"status": 1, "msg": "El pago se creo correctamente"}}
    if result == 3:
        raise HTTPException(status_code=500, detail= {"status": 3, "msg": "Ocurrió un error al crear el pago"}) 

@payment_routes.patch("/payment/{payment_id}", tags=["Payments"])
def patch_payment(payment_id:str,modify_payment:PaymentModify,db: Session = Depends(get_db)):

    result = update_payment_controller(db,payment_id, modify_payment)

    if result == 1:
        return {"detail": {"status": 1, "msg": "El pago se actualizó correctamente"}}
    if result == 3:
        raise HTTPException(status_code=500, detail= {"status": 3, "msg": "Ocurrió un error al actualizar el pago"}) 


@payment_routes.get("/payment_camper_camp/{camper_id}/{camp_id}", tags=["Payments"])    
def get_payment_camper_camp(camper_id: int, camp_id: int, db: Session= Depends(get_db)):

    list_payment = get_payment_by_camper_camp(db, camper_id, camp_id)    
    return {"data": list_payment}


@payment_routes.get("/payment/page/camper/{camper_id}/{camp_id}/{camper_in_camp_id}", tags=["Payments"])
def get_payment_page_camper_camp(camper_id:int, camp_id:int, camper_in_camp_id:int, db: Session = Depends(get_db)):
    data = get_payment_page_camper_in_camp(db, camper_id, camp_id, camper_in_camp_id)
    return data