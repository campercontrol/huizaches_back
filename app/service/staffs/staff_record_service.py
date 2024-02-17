from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.staffs.staff_record_crud import (
    get_all_staff_record,
    get_staff_record_by_id,
    create_new_staff_record,
    update_staff_record_by_id,
    get_record_by_staff_id
)

from schema.staffs.staff_record_schema import (
    StaffRecordCreate,
    StaffRecordModify,
)
from utils.db import SessionLocal

staff_record_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@staff_record_routes.get("/staff/record/", tags=["StaffRecord"])
def get_staff_record(db: Session = Depends(get_db)):
    list_staff_record = get_all_staff_record(db)
    return {"data": list_staff_record}


@staff_record_routes.get("/staff/record/{staff_record_id}", tags=["StaffRecord"])
def get_staff_record_by_uid(
    staff_record_id: str, db: Session = Depends(get_db)
):
    list_staff_record = get_staff_record_by_id(db, staff_record_id)
    return {"data": list_staff_record}


@staff_record_routes.post("/staff/record/", tags=["StaffRecord"])
def create_staff_record(
    new_staff_record: StaffRecordCreate, db: Session = Depends(get_db)
):
    list_staff_record = create_new_staff_record(db, new_staff_record)
    return {"data": list_staff_record}


@staff_record_routes.patch(
    "/staff/record/{staff_record_id}", tags=["StaffRecord"]
)
def update_staff_record(
    staff_record_id: int,
    modify_staff_record: StaffRecordModify,
    db: Session = Depends(get_db),
):
    update_data = modify_staff_record.dict(exclude_unset=True)
    print(update_data)
    camp_record_update_result = update_staff_record_by_id(
        db, staff_record_id, update_data
    )

    if camp_record_update_result != 0:
        exist_camp_record = get_staff_record_by_id(
            db, staff_record_id
        )
        return {"mensaje": "Actualizado Correctamente", "data": exist_camp_record}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@staff_record_routes.get("/staff/record/numbers/{staff_id}", tags=["StaffRecord"])
def record_numbers_by_staff(staff_id, db: Session = Depends(get_db)):
    number_records = get_record_by_staff_id(db, staff_id)
    return{"data": number_records}