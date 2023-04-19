from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.catalogs.licensed_medicine_crud import (
    get_all_licensed_medicine,
    get_licensed_medicine_by_uuid,
    create_new_licensed_medicine,
    update_licensed_medicine_by_id
)
from schema.catalogs.licensed_medicine_schema import(
    LicensedMedicineCreate,
    LicensedMedicineModify
)
from utils.db import SessionLocal

licensed_medicine_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@licensed_medicine_routes.get("/licensed_medicine/", tags=["Catalogs"])
def get_licensed_medicine(db: Session = Depends(get_db)):
    list_licensed_medicine = get_all_licensed_medicine(db)
    return {"data": list_licensed_medicine}


@licensed_medicine_routes.get("/licensed_medicine/{licensed_medicine_id}", tags=["Catalogs"])
def get_licensed_medicine_by_id(licensed_medicine_id:str,db: Session = Depends(get_db)):
    list_licensed_medicine = get_licensed_medicine_by_uuid(db,licensed_medicine_id)
    return {"data": list_licensed_medicine}


@licensed_medicine_routes.post("/licensed_medicine/", tags=["Catalogs"])
def create_licensed_medicine(new_prueba:LicensedMedicineCreate,db: Session = Depends(get_db)):
    list_licensed_medicine = create_new_licensed_medicine(db,new_prueba)
    return {"data": list_licensed_medicine}

@licensed_medicine_routes.post("/licensed_medicine/{licensed_medicine_id}", tags=["Catalogs"])
def update_licensed_medicine(licensed_medicine_id:str,modify_licensed_medicine:LicensedMedicineModify,db: Session = Depends(get_db)):

    update_data = modify_licensed_medicine.dict(exclude_unset=True)
    print(update_data)
    licensed_medicine_upcdate_result = update_licensed_medicine_by_id(db,licensed_medicine_id,update_data)

    if licensed_medicine_upcdate_result != 0:
        exist_licensed_medicine = get_licensed_medicine_by_uuid(db, licensed_medicine_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_licensed_medicine}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

