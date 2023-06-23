from sqlalchemy.exc import SQLAlchemyError

from model.catalogs import LicensedMedicine
from schema.catalogs.licensed_medicine_schema import (
    LicensedMedicineCreate,
    LicensedMedicineModify,
)
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case
from sqlalchemy.orm import Session


def get_all_licensed_medicine(db: Session):
    rows = db.query(LicensedMedicine).all()
    return rows


def get_all_licensed_medicine_id_name(db: Session):
    rows = db.query(LicensedMedicine.id, LicensedMedicine.name).all()
    return db_mapping_rows_to_dict(rows)


def get_licensed_medicine_by_uuid(db, licensed_medicine_id):
    return (
        db.query(LicensedMedicine)
        .filter_by(
            id=licensed_medicine_id,
        )
        .first()
    )


def create_new_licensed_medicine(
    db: Session, new_licensed_medicine: LicensedMedicineCreate
):
    db_licensed_medicine = None
    try:
        db_licensed_medicine = LicensedMedicine(
            id=new_licensed_medicine.id,
            name=new_licensed_medicine.name,
            assigned_id=new_licensed_medicine.assigned_id,
            order=new_licensed_medicine.order,
            created_at=new_licensed_medicine.created_at,
        )
        db.add(db_licensed_medicine)
        db.commit()
        db.refresh(db_licensed_medicine)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_licensed_medicine = None
        return db_licensed_medicine
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_licensed_medicine


def update_licensed_medicine_by_id(
    db: Session,
    licensed_medicine_id: int,
    modify_licensed_medicine: LicensedMedicineModify,
):
    rows_updated = (
        db.query(LicensedMedicine)
        .filter_by(id=licensed_medicine_id)
        .update(modify_licensed_medicine, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def delete_licensed_medicine(db: Session, licensed_medicine_id:int):
    licensed_medicine = db.query(LicensedMedicine).filter(LicensedMedicine.id==licensed_medicine_id).first()
    db.delete(licensed_medicine)
    db.commit()
    return {"status" : True}