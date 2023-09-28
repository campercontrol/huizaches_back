from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.trainings import Training
from schema.trainings.training_schema import TrainingCreate, TrainingModify


def get_all_training(db: Session):
    rows = db.query(Training).all()
    return rows


def get_all_active_training(db: Session):
    rows = db.query(Training).filter_by(active=True).all()
    return rows

def get_training_by_id(db: Session, training_id: int):
    return db.query(Training).filter_by(id=training_id).first()

def create_new_training(db: Session, new_training: TrainingCreate):
    db_training = None
    try:
        db_training = Training(**new_training.dict())
        db.add(db_training)
        db.commit()
        db.refresh(db_training)
    except SQLAlchemyError as e:
        print("#========================#")
        print(e)
        print("#========================#")
        db_training = None
        return db_training
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_training


def update_training_by_id(db: Session, training_id: int, modify_training: TrainingModify):
    rows_updated = (
        db.query(Training)
        .filter_by(id=training_id)
        .update(modify_training, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

