from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.campers import CamperLicensedMedicine
from schema.campers_catalogs.camper_licensed_medicine_schema import (
    CamperLicensedMedicineCreate,
    CamperLicensedMedicineModify,
)


def get_all_camper_licensed_medicine(db: Session):
    rows = db.query(CamperLicensedMedicine).all()
    return rows


def get_all_camper_licensed_medicine_id_name(db: Session):
    rows = db.query(CamperLicensedMedicine.id, CamperLicensedMedicine.name).all()
    return db_mapping_rows_to_dict(rows)


def get_camper_licensed_medicine_by_uuid(db: Session, camper_licensed_medicine_id: int):
    return (
        db.query(CamperLicensedMedicine)
        .filter_by(
            id=camper_licensed_medicine_id,
        )
        .first()
    )


def create_new_camper_licensed_medicine(
    db: Session, new_camper_licensed_medicine: CamperLicensedMedicineCreate
):
    db_camper_licensed_medicine = None
    try:
        db_camper_licensed_medicine = CamperLicensedMedicine(
            id=new_camper_licensed_medicine.id,
            camper_id=new_camper_licensed_medicine.camper_id,
            licensed_medicine_id=new_camper_licensed_medicine.licensed_medicine_id,
            is_active=new_camper_licensed_medicine.is_active,
        )
        db.add(db_camper_licensed_medicine)
        db.commit()
        db.refresh(db_camper_licensed_medicine)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_licensed_medicine = None
        return db_camper_licensed_medicine
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_licensed_medicine


def update_camper_licensed_medicine_by_ids(
    db: Session,
    camper_licensed_medicine_id: int,
    camper_id:int, 
    modify_camper_licensed_medicine: CamperLicensedMedicineModify,
):
    rows_updated = (
        db.query(CamperLicensedMedicine)
        .filter_by(licensed_medicine_id=camper_licensed_medicine_id, camper_id=camper_id)
        .update(modify_camper_licensed_medicine, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
