from sqlalchemy.exc import SQLAlchemyError

from model.catalogs import LicensedMedicine
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_licensed_medicine(db):
    rows = db.query(LicensedMedicine).all()
    return rows

def get_licensed_medicine_by_uuid(db, licensed_medicine_id):
    return (
        db.query(LicensedMedicine)
        .filter_by(
            id=licensed_medicine_id,
        )
        .first()
    )


def create_new_licensed_medicine(db, new_licensed_medicine):
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


def update_licensed_medicine_by_id(db, licensed_medicine_id, modify_licensed_medicine):
    rows_updated = (
        db.query(LicensedMedicine).filter_by(id=licensed_medicine_id).update(modify_licensed_medicine, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
