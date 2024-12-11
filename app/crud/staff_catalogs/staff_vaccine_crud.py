from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.staffs import StaffVaccine
from schema.staff_catalogs.staff_vaccine_schema import (
    StaffVaccineCreate,
    StaffVaccineModify,
)


def get_all_staff_vaccine(db: Session):
    rows = db.query(StaffVaccine).all()
    return rows


def get_all_staff_vaccine_id_name(db: Session):
    rows = db.query(StaffVaccine.id, StaffVaccine.name).all()
    return db_mapping_rows_to_dict(rows)


def get_staff_vaccine_by_uuid(db: Session, staff_vaccine_id: int):
    return (
        db.query(StaffVaccine)
        .filter_by(
            id=staff_vaccine_id,
        )
        .first()
    )

def get_staff_all_vaccines_by_staff_id(db: Session, staff_id: int):    
    rows = db.query(StaffVaccine).filter(StaffVaccine.staff_id == staff_id).all()
    return rows


def get_staff_vaccine_by_vaccine(db: Session, vaccine_id: int):
    return (
        db.query(StaffVaccine)
        .filter_by(
            vaccine_id=vaccine_id,
        )
        .first()
    )


def create_new_staff_vaccine(db: Session, new_staff_vaccine: StaffVaccineCreate):
    db_staff_vaccine = None
    try:
        db_staff_vaccine = StaffVaccine(**new_staff_vaccine.dict())
        db.add(db_staff_vaccine)
        db.commit()
        db.refresh(db_staff_vaccine)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_staff_vaccine = None
        return db_staff_vaccine
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_staff_vaccine


def update_staff_vaccine_by_id(
    db: Session,
    staff_vaccine_id: int,
    staff_id: int,
    modify_staff_vaccine: StaffVaccineModify,
):
    print("######################################################")
    print(type(modify_staff_vaccine))
    rows_updated = (
        db.query(StaffVaccine)
        .filter_by(vaccine_id=staff_vaccine_id, staff_id=staff_id)
        .update(modify_staff_vaccine, synchronize_session="fetch")
    )
    print(rows_updated)
    db.commit()
    return rows_updated
