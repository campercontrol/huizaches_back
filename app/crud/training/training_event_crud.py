from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.trainings import TrainingEvent
from schema.trainings.training_event_schema import (
    TrainingEventCreate,
    TrainingEventModify
)


def get_all_training_event(db: Session):
    rows = db.query(TrainingEvent).all()
    return rows


def get_all_active_training_event(db: Session):
    rows = db.query(TrainingEvent).filter_by(active=True).all()
    return rows

def get_training_event_by_id(db: Session, training_event_id: int):
    return db.query(TrainingEvent).filter_by(id=training_event_id).first()

def create_new_training_event(db: Session, new_training_event: TrainingEventCreate):
    db_training_event = None
    try:
        db_training_event = TrainingEvent(**new_training_event.dict())
        db.add(db_training_event)
        db.commit()
        db.refresh(db_training_event)
    except SQLAlchemyError as e:
        print("#========================#")
        print(e)
        print("#========================#")
        db_training_event = None
        return db_training_event
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_training_event


def update_training_event_by_id(db: Session, training_event_id: int, modify_training_event: TrainingEventModify):
    rows_updated = (
        db.query(TrainingEvent)
        .filter_by(id=training_event_id)
        .update(modify_training_event, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

