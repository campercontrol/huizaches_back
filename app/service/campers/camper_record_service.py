from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.campers.camper_record_crud import (
    get_all_camper_record,
    get_camper_record_by_id,
    create_new_camper_record,
    update_camper_record_by_id,
    get_record_by_camper_id
)

from schema.campers.camper_record_schema import (
    CamperRecordCreate,
    CamperRecordModify,
)
from utils.db import SessionLocal

camper_record_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@camper_record_routes.get("/camper_record/", tags=["CamperRecord"])
def get_camper_record(db: Session = Depends(get_db)):
    list_camper_record = get_all_camper_record(db)
    return {"data": list_camper_record}


@camper_record_routes.get("/camper_record/{camper_record_id}", tags=["CamperRecord"])
def get_camper_record_by_uid(
    camper_record_id: str, db: Session = Depends(get_db)
):
    list_camper_record = get_camper_record_by_id(db, camper_record_id)
    return {"data": list_camper_record}


@camper_record_routes.post("/camper_record/", tags=["CamperRecord"])
def create_camper_record(
    new_camper_record: CamperRecordCreate, db: Session = Depends(get_db)
):
    list_camper_record = create_new_camper_record(db, new_camper_record)
    return {"data": list_camper_record}


@update_camper_record_by_id.patch(
    "/camper_record/{camper_record_id}", tags=["CamperRecord"]
)
def update_camper_record(
    camper_record_id: int,
    modify_camper_record: CamperRecordModify,
    db: Session = Depends(get_db),
):
    update_data = modify_camper_record.dict(exclude_unset=True)
    print(update_data)
    camp_record_update_result = update_camper_record_by_id(
        db, camper_record_id, update_data
    )

    if camp_record_update_result != 0:
        exist_camp_record = get_camper_record_by_id(
            db, camper_record_id
        )
        return {"mensaje": "Actualizado Correctamente", "data": exist_camp_record}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@camper_record_routes.get("/camper_record_numbers/{camper_id}", tags=["CamperRecord"])
def record_numbers_by_camper(camper_id, db: Session = Depends(get_db)):
    number_records = get_record_by_camper_id(db, camper_id)
    return{"data": number_records}