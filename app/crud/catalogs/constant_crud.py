from sqlalchemy.exc import SQLAlchemyError

from model.catalogs import Constant
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_constant(db):
    rows = db.query(Constant).all()
    return rows

def get_constant_by_uuid(db, constant_id):
    return (
        db.query(Constant)
        .filter_by(
            id=constant_id,
        )
        .first()
    )


def create_new_constant(db, new_constant):
    db_constant = None
    try:
        db_constant = Constant(
            id=new_constant.id,
            value=new_constant.value,
            num_id=new_constant.num_id,
            language=new_constant.language,
            model_name=new_constant.model_name,
            created_at=new_constant.created_at,
        )
        db.add(db_constant)
        db.commit()
        db.refresh(db_constant)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_constant = None
        return db_constant
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_constant


def update_constant_by_id(db, constant_id, modify_constant):
    rows_updated = (
        db.query(Constant).filter_by(id=constant_id).update(modify_constant, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
