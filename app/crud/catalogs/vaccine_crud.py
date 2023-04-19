from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.catalogs import Vaccine
from schema.catalogs.vaccine_schema import VaccineCreate, VaccineModify


def get_all_vaccine(db: Session):
    rows = db.query(Vaccine).all()
    return rows


def get_all_vaccine_id_name(db: Session):
    rows = db.query(Vaccine.id, Vaccine.name).all()
    return db_mapping_rows_to_dict(rows)


def get_vaccine_by_uuid(db: Session, vaccine_id: int):
    return (
        db.query(Vaccine)
        .filter_by(
            id=vaccine_id,
        )
        .first()
    )


def create_new_vaccine(db: Session, new_vaccine: VaccineCreate):
    db_vaccine = None
    try:
        db_vaccine = Vaccine(
            id=new_vaccine.id,
            name=new_vaccine.name,
            assigned_id=new_vaccine.assigned_id,
            order=new_vaccine.order,
            created_at=new_vaccine.created_at,
        )
        db.add(db_vaccine)
        db.commit()
        db.refresh(db_vaccine)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_vaccine = None
        return db_vaccine
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_vaccine


def update_vaccine_by_id(db: Session, vaccine_id: int, modify_vaccine: VaccineModify):
    rows_updated = (
        db.query(Vaccine)
        .filter_by(id=vaccine_id)
        .update(modify_vaccine, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
