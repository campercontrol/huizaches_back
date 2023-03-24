from sqlalchemy.exc import SQLAlchemyError

from model.prueba import Prueba
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_prueba(db):
    rows = db.query(Prueba).all()
    return rows

def get_prueba_by_uuid(db, prueba_id):
    return (
        db.query(Prueba)
        .filter_by(
            id=prueba_id,
        )
        .first()
    )


def create_new_prueba(db, new_prueba):
    db_prueba = None
    try:
        db_prueba = Prueba(
            name_prueba=new_prueba.name_prueba
        )
        db.add(db_prueba)
        db.commit()
        db.refresh(db_prueba)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_prueba = None
        return db_prueba
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_prueba


def update_prueba_by_id(db, prueba_id, modify_prueba):
    rows_updated = (
        db.query(Prueba).filter_by(id=prueba_id).update(modify_prueba, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
