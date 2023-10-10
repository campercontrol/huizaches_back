from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.trainings import StaffInTraining, Training, TrainingEvent
from model.staffs import Staff
from model.user import User
from schema.trainings.staff_in_training_schema import (
    StaffInTrainingCreate,
    StaffInTrainingModify,
)


def get_all_staff_in_training_event(db: Session, training_event_id: int):
    staffs = (
        db.query(Staff.name, User.email)
        .join(User, User.id == Staff.login_id)
        .join(Staff, Staff.id == StaffInTraining.staff_id)
        .filter(StaffInTraining.training_event_id == training_event_id)
        .all()
    )
    return db_mapping_rows_to_dict(staffs)

def get_all_staff_in_training(db: Session):
    rows = db.query(StaffInTraining).all()
    return rows


def create_new_staff_in_training(
    db: Session, new_staff_in_training: StaffInTrainingCreate
):
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

        training_event = (
            db.query(TrainingEvent)
            .filter(TrainingEvent.id == db_staff_in_training.training_event_id)
            .first()
        )

        if training_event.open_enrollment == True:
            db_staff_in_training.confirmed_staff = True
        else:
            db_staff_in_training.confirmed_staff = False

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


def unsubscribe_staff(db: Session, id_staff_in_training: int):
    db.query(StaffInTraining).filter_by(id=id_staff_in_training).delete()
    db.commit()
    return


def staff_training_dashboard(db, staff_id: int):
    trainings_id = []
    trainings_events_id = []

    confirmed_trainings = (
        db.query(
            Training.name.label("training_name"),
            TrainingEvent.location.label("training_event_location"),
            Training.id.label("training_id"),
            TrainingEvent.id.label("training_event_id"),
        )
        .join(Training, TrainingEvent.training_id == Training.id)
        .join(StaffInTraining, StaffInTraining.training_event_id == TrainingEvent.id)
        .filter(
            and_(
                StaffInTraining.staff_id == staff_id,
                StaffInTraining.confirmed_staff == True,
                TrainingEvent.active == True,
                TrainingEvent.start >= date.today(),
                Training.active == True,
            )
        )
        .all()
    )

    confirmed_trainings = db_mapping_rows_to_dict(confirmed_trainings)

    for confimed_training in confirmed_trainings:
        if confimed_training["training_id"] not in trainings_id:
            trainings_id.append(confimed_training["training_id"])

    for confimed_training in confirmed_trainings:
        if confimed_training["training_event_id"] not in trainings_events_id:
            trainings_events_id.append(confimed_training["training_event_id"])

    available_trainings = (
        db.query(
            Training.name.label("training_name"),
            TrainingEvent.location.label("training_event_location"),
            Training.id.label("training_id"),
            TrainingEvent.id.label("training_event_id"),
        )
        .join(Training, TrainingEvent.training_id == Training.id)
        .join(StaffInTraining, StaffInTraining.training_event_id == TrainingEvent.id)
        .filter(
            and_(
                StaffInTraining.staff_id == staff_id,
                StaffInTraining.confirmed_staff == False,
                TrainingEvent.active == True,
                TrainingEvent.start >= date.today(),
                Training.active == True,
            )
        )
        .all()
    )

    available_trainings = db_mapping_rows_to_dict(available_trainings)

    for available_training in available_trainings:
        if available_training["training_id"] not in trainings_id:
            trainings_id.append(available_training["training_id"])

    for available_training in available_trainings:
        if available_training["training_event_id"] not in trainings_events_id:
            trainings_events_id.append(available_training["training_event_id"])

    next_trainings = (
        db.query(
            Training.name.label("training_name"),
            TrainingEvent.start.label("training_event_start"),
            TrainingEvent.end.label("training_event_end"),
            TrainingEvent.location.label("training_event_location"),
            Training.id.label("training_id"),
            TrainingEvent.id.label("training_event_id"),
        )
        .join(Training, TrainingEvent.training_id == Training.id)
        .filter(
            TrainingEvent.id.not_in(trainings_events_id),
            TrainingEvent.active == True,
            TrainingEvent.start >= date.today(),
            Training.active == True,
        )
    )

    next_trainings = db_mapping_rows_to_dict(next_trainings)

    for nex_training in next_trainings:
        if nex_training["training_id"] not in trainings_id:
            trainings_id.append(nex_training["training_id"])

    trainings = db.query(
        Training.name.label("training_name"),
        Training.description.label("training_description"),
        Training.id.label("training_id"),
    ).filter(Training.active == True, Training.id.not_in(trainings_id))

    trainings = db_mapping_rows_to_dict(trainings)

    return {
        "confirmed_trainings": confirmed_trainings,
        "available_trainings": available_trainings,
        "next_trainings": next_trainings,
        "trainings": trainings,
    }
