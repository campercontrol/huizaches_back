from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.catalogs import PathologicalBackgroundFamily
from schema.catalogs.pathological_back_fm_schema import (
    PathologicalBackgroundFamilyCreate,
    PathologicalBackgroundFamilyModify,
)


def get_all_pathological_background_family(db: Session):
    rows = db.query(PathologicalBackgroundFamily).all()
    return rows


def get_all_pathological_background_family_id_name(db: Session):
    rows = db.query(
        PathologicalBackgroundFamily.id, PathologicalBackgroundFamily.name
    ).all()
    return db_mapping_rows_to_dict(rows)


def get_pathological_background_family_by_uuid(
    db: Session, pathological_background_family_id: int
):
    return (
        db.query(PathologicalBackgroundFamily)
        .filter_by(
            id=pathological_background_family_id,
        )
        .first()
    )


def create_new_pathological_background_family(
    db: Session, new_pathological_background_family: PathologicalBackgroundFamilyCreate
):
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


def update_pathological_background_family_by_id(
    db: Session,
    pathological_background_family_id: int,
    modify_pathological_background_family: PathologicalBackgroundFamilyModify,
):
    rows_updated = (
        db.query(PathologicalBackgroundFamily)
        .filter_by(id=pathological_background_family_id)
        .update(modify_pathological_background_family, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def delete_pathological_back_fm(db: Session, pathological_back_fm_id:int):
    pathological_back_fm = db.query(PathologicalBackgroundFamily).filter(PathologicalBackgroundFamily.id==pathological_back_fm_id).first()
    db.delete(pathological_back_fm)
    db.commit()
    return {"status" : True}