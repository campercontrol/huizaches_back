from sqlalchemy.exc import SQLAlchemyError

from model.catalogs import PathologicalBackgroundFamily
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_pathological_background_family(db):
    rows = db.query(PathologicalBackgroundFamily).all()
    return rows

def get_pathological_background_family_by_uuid(db, pathological_background_family_id):
    return (
        db.query(PathologicalBackgroundFamily)
        .filter_by(
            id=pathological_background_family_id,
        )
        .first()
    )


def create_new_pathological_background_family(db, new_pathological_background_family):
    db_pathological_background_family = None
    try:
        db_pathological_background_family = PathologicalBackgroundFamily(
            id=new_pathological_background_family.id,
            name=new_pathological_background_family.name,
            assigned_id=new_pathological_background_family.assigned_id,
            order=new_pathological_background_family.order,
            created_at=new_pathological_background_family.created_at,
        )
        db.add(db_pathological_background_family)
        db.commit()
        db.refresh(db_pathological_background_family)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_pathological_background_family = None
        return db_pathological_background_family
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_pathological_background_family


def update_pathological_background_family_by_id(db, pathological_background_family_id, modify_pathological_background_family):
    rows_updated = (
        db.query(PathologicalBackgroundFamily).filter_by(id=pathological_background_family_id).update(modify_pathological_background_family, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
