from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.payments.camper_extra_charge_crud import (
    get_all_camper_extra_charge,
    get_camper_extra_charge_by_id,
    update_camper_extra_charge_by_id,
    create_new_camper_extra_charge,
    get_extra_charge_by_camper_camp,
    create_update_extra_charges
    
)
from schema.payments.camper_extra_charge_schema import(
    CamperExtraChargeCreate,
    CamperExtraChargeModify,
    CamperExtraChargeListCreate
)
from utils.db import SessionLocal

camper_extra_charge_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@camper_extra_charge_routes.get("/camper_extra_charge/", tags=["Payments"])
def get_camper_extra_charge(db: Session = Depends(get_db)):
    list_camper_extra_charge = get_all_camper_extra_charge(db)
    return {"data": list_camper_extra_charge}

@camper_extra_charge_routes.get("/camper_extra_charge/{payment_id}", tags=["Payments"])
def get_camper_extra_charge_by__id(payment_id:str,db: Session = Depends(get_db)):
    payment = get_camper_extra_charge_by_id(db,payment_id)
    return {"data": payment}

@camper_extra_charge_routes.post("/camper_extra_charge/", tags=["Payments"])
def create_camper_extra_charge(new_camper_extra_charge:CamperExtraChargeCreate,db: Session = Depends(get_db)):
    payment = create_new_camper_extra_charge(db, new_camper_extra_charge)
    return {"data": payment}

@camper_extra_charge_routes.patch("/camper_extra_charge/{payment_id}", tags=["Payments"])
def update_camper_extra_charge(payment_id:str,modify_camper_extra_charge:CamperExtraChargeModify,db: Session = Depends(get_db)):

    update_data = modify_camper_extra_charge.dict(exclude_unset=True)
    print(update_data)
    payment_update_result = update_camper_extra_charge_by_id(db,payment_id,update_data)

    if payment_update_result != 0:
        exist_camper_extra_charge = get_camper_extra_charge_by_id(db, payment_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_camper_extra_charge}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@camper_extra_charge_routes.get("/camper_extra_charge_by_camp/{camper_id}/{camp_id}", tags=["Payments"])
def get_camper_extra_charge_camp(camper_id:int, camp_id:int, db: Session = Depends(get_db)):
    extras = get_extra_charge_by_camper_camp(db, camper_id, camp_id)
    return {"data": extras}

@camper_extra_charge_routes.post("/camper/extra_charges/", tags=["Payments"])
def set_extra_charges_camper(camper_extras: CamperExtraChargeListCreate, db: Session= Depends(get_db)):    
    extras = create_update_extra_charges(db, camper_extras)
    return {"data":"ok"}