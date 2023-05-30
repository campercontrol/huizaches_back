from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.camps.staff_in_camp_crud import (
    get_all_staff_in_camp,
    create_new_staff_in_camp,
    volunteer_staff,
    unsubscribe_staff
)
from schema.camps.staff_in_camp_schema import(
    StaffInCampCreate,
    StaffInCampModify
)
from utils.db import SessionLocal

staff_in_camp_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@staff_in_camp_routes.get("/staff_in_camp/", tags=["StaffInCamp"])
def get_staff_in_camp(db: Session = Depends(get_db)):
    list_staff_in_camp = get_all_staff_in_camp(db)
    return {"data": list_staff_in_camp}


@staff_in_camp_routes.post("/staff_in_camp/", tags=["StaffInCamp"])
def create_staff_in_camp(new_staff_in_camp:StaffInCampCreate,db: Session = Depends(get_db)):
    staff_in_camp = create_new_staff_in_camp(db, new_staff_in_camp)
    return {"data": staff_in_camp}

@staff_in_camp_routes.post("/staff_volunteer/", tags=["StaffInCamp"])
def create_staff_volunteer(new_staff_in_camp:StaffInCampCreate, db: Session = Depends(get_db)):
    staff_in_camp = volunteer_staff(db, new_staff_in_camp)
    return {"data": staff_in_camp}

@staff_in_camp_routes.delete("/staff_unsubscribe/{id_staff_in_camp}", tags=["StaffInCamp"])
def unsubscribe_staff_to_camp(id_staff_in_camp:int , db: Session = Depends(get_db)):
    staff_in_camp = unsubscribe_staff(db, id_staff_in_camp)
    return {"data": staff_in_camp}