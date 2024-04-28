from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.campers import CamperVaccine
from schema.campers_catalogs.camper_vaccine_schema import (
    CamperVaccineCreate,
    CamperVaccineModify,
)


def get_all_camper_vaccine(db: Session):
    rows = db.query(CamperVaccine).all()
    return rows


def get_all_camper_vaccine_id_name(db: Session):
    rows = db.query(CamperVaccine.id, CamperVaccine.name).all()
    return db_mapping_rows_to_dict(rows)


def get_camper_vaccine_by_uuid(db: Session, camper_vaccine_id: int):
    return (
        db.query(CamperVaccine)
        .filter_by(
            id=camper_vaccine_id,
        )
        .first()
    )


def create_new_camper_vaccine(db: Session, new_camper_vaccine: CamperVaccineCreate):
    db_camper_vaccine = None
    try:
        db_camper_vaccine = CamperVaccine(
            id=new_camper_vaccine.id,
            camper_id=new_camper_vaccine.camper_id,
            vaccine_id=new_camper_vaccine.vaccine_id,
            is_active=new_camper_vaccine.is_active,
        )
        db.add(db_camper_vaccine)
        db.commit()
        db.refresh(db_camper_vaccine)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_vaccine = None
        return db_camper_vaccine
    except Exception as ex:
        db.rollback()
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_vaccine


def update_camper_vaccine_by_ids(
    db: Session,
    camper_vaccine_id: int,
    camper_id: int,
    modify_camper_vaccine: CamperVaccineModify,
):
    print("######################################################")
    print(type(modify_camper_vaccine))
    rows_updated = (
        db.query(CamperVaccine)
        .filter_by(vaccine_id=camper_vaccine_id, camper_id=camper_id)
        .update(modify_camper_vaccine, synchronize_session="fetch")
    )
    print(rows_updated)
    db.commit()
    return rows_updated
