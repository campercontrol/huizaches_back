from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.trainings import StaffInTraining
from schema.trainings.staff_in_training_schema import (
    StaffInTrainingCreate,
    StaffInTrainingModify,
)


def get_all_staff_in_training(db: Session):
    rows = db.query(StaffInTraining).all()
    return rows


def create_new_staff_in_training(db: Session, new_staff_in_training: StaffInTrainingCreate):
    db_staff_in_training = None
    try:
        db_staff_in_training = StaffInTraining(**new_staff_in_training.dict())
        db.add(db_staff_in_training)
        db.commit()
        db.refresh(db_staff_in_training)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_staff_in_training = None
        return db_staff_in_training
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_staff_in_training


def volunteer_staff(db: Session, new_staff_in_training: StaffInTrainingCreate):
    db_staff_in_training = None
    try:
        db_staff_in_training = StaffInTraining(**new_staff_in_training.dict())
        db_staff_in_training.confirmed_staff= False
        db.add(db_staff_in_training)
        db.commit()
        db.refresh(db_staff_in_training)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_staff_in_training = None
        return db_staff_in_training
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_staff_in_training


def unsubscribe_staff(db:Session, id_staff_in_training: int):
    db.query(StaffInTraining).filter_by(id=id_staff_in_training).delete()
    db.commit()
    return