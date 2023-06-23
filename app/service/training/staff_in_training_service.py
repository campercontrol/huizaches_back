from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.training.staff_in_training_crud import (
    get_all_staff_in_training,
    create_new_staff_in_training,
    volunteer_staff,
    unsubscribe_staff,
    staff_training_dashboard
)
from schema.trainings.staff_in_training_schema import(
    StaffInTrainingCreate,
    StaffInTrainingModify
)
from utils.db import SessionLocal

staff_in_training_router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@staff_in_training_router.get("/staff_in_training/", tags=["StaffInTraining"])
def get_staff_in_training(db: Session = Depends(get_db)):
    list_staff_in_training = get_all_staff_in_training(db)
    return {"data": list_staff_in_training}


@staff_in_training_router.post("/staff_in_training/", tags=["StaffInTraining"])
def create_staff_in_training(new_staff_in_training:StaffInTrainingCreate,db: Session = Depends(get_db)):
    staff_in_training = create_new_staff_in_training(db, new_staff_in_training)
    return {"data": staff_in_training}

@staff_in_training_router.post("/staff_volunteer_training/", tags=["StaffInTraining"])
def create_staff_volunteer(new_staff_in_training:StaffInTrainingCreate, db: Session = Depends(get_db)):
    staff_in_training = volunteer_staff(db, new_staff_in_training)
    return {"data": staff_in_training}

@staff_in_training_router.delete("/staff_unsubscribe_training/{id_staff_in_training}", tags=["StaffInTraining"])
def unsubscribe_staff_to_camp(id_staff_in_training:int , db: Session = Depends(get_db)):
    staff_in_training = unsubscribe_staff(db, id_staff_in_training)
    return {"data": staff_in_training}

@staff_in_training_router.get("/staff/dashboard_trainig/{staff_id}", tags=["StaffInTraining"])
def get_staff_dashboard_training(staff_id:int, db: Session = Depends(get_db)):
    training_dashboard = staff_training_dashboard(db, staff_id)
    return {"data": training_dashboard }