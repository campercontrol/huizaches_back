from sqlalchemy.exc import SQLAlchemyError

from model.catalogs import Vaccine
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_vaccine(db):
    rows = db.query(Vaccine).all()
    return rows

def get_vaccine_by_uuid(db, vaccine_id):
    return (
        db.query(Vaccine)
        .filter_by(
            id=vaccine_id,
        )
        .first()
    )


def create_new_vaccine(db, new_vaccine):
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


def update_vaccine_by_id(db, vaccine_id, modify_vaccine):
    rows_updated = (
        db.query(Vaccine).filter_by(id=vaccine_id).update(modify_vaccine, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
