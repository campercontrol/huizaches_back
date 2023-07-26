from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.camps.camp_extra_charge_crud import (
    get_all_extra_charge,
    get_extra_charge_by_id,
    get_extra_charge_by_camp,
    create_new_extra_charge,
    update_extra_charge_by_id,
)

from schema.camps.camp_extra_charge_schema import (
    CampExtraChargeCreate,
    CampExtraChargeModify,
)
from utils.db import SessionLocal

extra_charge_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@extra_charge_routes.get("/camp_extra_charge/", tags=["CampsExtraCharge"])
def get_camp_extra_charge(db: Session = Depends(get_db)):
    list_camp_extra_charge = get_all_extra_charge(db)
    return {"data": list_camp_extra_charge}


@extra_charge_routes.get("/camp_extra_charge/{camp_extra_charge_id}", tags=["CampsExtraCharge"])
def get_camp_extra_charge_by_id(
    camp_extra_charge_id: str, db: Session = Depends(get_db)
):
    list_camp_extra_charge = get_extra_charge_by_id(db, camp_extra_charge_id)
    return {"data": list_camp_extra_charge}


@extra_charge_routes.post("/camp_extra_charge/", tags=["CampsExtraCharge"])
def create_camp_extra_charge(
    new_camp_extra_charge: CampExtraChargeCreate, db: Session = Depends(get_db)
):
    list_camp_extra_charge = create_new_extra_charge(db, new_camp_extra_charge)
    return {"data": list_camp_extra_charge}


@extra_charge_routes.patch(
    "/camp_extra_charge/{camp_extra_charge_id}", tags=["CampsExtraCharge"]
)
def update_camp_extra_charge(
    camp_extra_charge_id: int,
    modify_camp_extra_charge: CampExtraChargeModify,
    db: Session = Depends(get_db),
):
    update_data = modify_camp_extra_charge.dict(exclude_unset=True)
    print(update_data)
    camp_extra_charge_update_result = update_extra_charge_by_id(
        db, camp_extra_charge_id, update_data
    )

    if camp_extra_charge_update_result != 0:
        exist_camp_extra_charge = get_camp_extra_charge_by_id(
            db, camp_extra_charge_id
        )
        return {"mensaje": "Actualizado Correctamente", "data": exist_camp_extra_charge}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@extra_charge_routes.get("/extra_charge_by_camp/{camp_id}", tags=["CampsExtraCharge"])
def extra_charge_bycamp(camp_id, db: Session = Depends(get_db)):
    list_extra_charges = get_extra_charge_by_camp(db, camp_id)
    return{"data": list_extra_charges}