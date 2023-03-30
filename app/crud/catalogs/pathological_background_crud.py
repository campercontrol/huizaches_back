from sqlalchemy.exc import SQLAlchemyError

from model.catalogs import PathologicalBackground
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_pathological_background(db):
    rows = db.query(PathologicalBackground).all()
    return rows

def get_pathological_background_by_uuid(db, pathological_background_id):
    return (
        db.query(PathologicalBackground)
        .filter_by(
            id=pathological_background_id,
        )
        .first()
    )


def create_new_pathological_background(db, new_pathological_background):
    db_pathological_background = None
    try:
        db_pathological_background = PathologicalBackground(
            id=new_pathological_background.id,
            name=new_pathological_background.name,
            assigned_id=new_pathological_background.assigned_id,
            order=new_pathological_background.order,
            created_at=new_pathological_background.created_at,            
        )
        db.add(db_pathological_background)
        db.commit()
        db.refresh(db_pathological_background)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_pathological_background = None
        return db_pathological_background
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_pathological_background


def update_pathological_background_by_id(db, pathological_background_id, modify_pathological_background):
    rows_updated = (
        db.query(PathologicalBackground).filter_by(id=pathological_background_id).update(modify_pathological_background, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
