from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.catalogs import PathologicalBackground
from schema.catalogs.pathological_back_schema import (
    PathologicalBackgroundCreate,
    PathologicalBackgroundModify,
)


def get_all_pathological_background(db: Session):
    rows = db.query(PathologicalBackground).all()
    return rows


def get_all_pathological_background_id_name(db: Session):
    rows = db.query(PathologicalBackground.id, PathologicalBackground.name).all()
    return db_mapping_rows_to_dict(rows)


def get_pathological_background_by_uuid(db: Session, pathological_background_id: int):
    return (
        db.query(PathologicalBackground)
        .filter_by(
            id=pathological_background_id,
        )
        .first()
    )


def create_new_pathological_background(
    db: Session, new_pathological_background: PathologicalBackgroundCreate
):
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


def update_pathological_background_by_id(
    db: Session,
    pathological_background_id: int,
    modify_pathological_background: PathologicalBackgroundModify,
):
    rows_updated = (
        db.query(PathologicalBackground)
        .filter_by(id=pathological_background_id)
        .update(modify_pathological_background, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
