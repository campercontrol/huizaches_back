from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from crud.training.training_event_crud import (
    get_all_training_event,
    get_all_active_training_event,
    get_training_event_by_id,
     create_new_training_event,
    update_training_event_by_id,
)

from schema.trainings.training_event_schema import TrainingEventCreate, TrainingEventModify


from utils.db import SessionLocal

training_event_router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@training_event_router.get("/training_event/", tags=["Trainings"])
def get_training_event(db: Session = Depends(get_db)):
    list_training_event = get_all_training_event(db)
    return {"data": list_training_event}


@training_event_router.get("/active_training_event/", tags=["Trainings"])
def get__active_training_event(db: Session = Depends(get_db)):
    list_training_event = get_all_active_training_event(db)
    return {"data": list_training_event}


@training_event_router.post("/training_event/", tags=["Trainings"])
def create_training_event(new_training_event: TrainingEventCreate, db: Session = Depends(get_db)):
    training_event =  create_new_training_event(db, new_training_event)
    return {"data": training_event}


@training_event_router.patch("/training_event/{training_event_id}", tags=["Trainings"])
def update_training_event(training_event_id: int, modify_training_event: TrainingEventModify, db: Session = Depends(get_db)):
    update_data = modify_training_event.dict(exclude_unset=True)
    training_event_update_result = update_training_event_by_id(db, training_event_id, update_data)

    if training_event_update_result != 0:
        exist_training_event = get_training_event_by_id(db, training_event_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_training_event}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}
