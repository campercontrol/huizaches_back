from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from crud.training.training_crud import (
    get_all_training,
    get_all_active_training,
    get_training_by_id,
     create_new_training,
    update_training_by_id,
)

from schema.trainings.training_schema import TrainingCreate, TrainingModify


from utils.db import SessionLocal

training_router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@training_router.get("/training/", tags=["Trainings"])
def get_training(db: Session = Depends(get_db)):
    list_training = get_all_training(db)
    return {"data": list_training}


@training_router.get("/active_training/", tags=["Trainings"])
def get__active_training(db: Session = Depends(get_db)):
    list_training = get_all_active_training(db)
    return {"data": list_training}


@training_router.post("/training/", tags=["Trainings"])
def create_training(new_training: TrainingCreate, db: Session = Depends(get_db)):
    training =  create_new_training(db, new_training)
    return {"data": training}


@training_router.patch("/training/{training_id}", tags=["Trainings"])
def update_training(training_id: int, modify_training: TrainingModify, db: Session = Depends(get_db)):
    update_data = modify_training.dict(exclude_unset=True)
    training_update_result = update_training_by_id(db, training_id, update_data)

    if training_update_result != 0:
        exist_training = get_training_by_id(db, training_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_training}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}
