from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.campers import CamperPathologicalBackground
from schema.campers_catalogs.camper_pathological_background_schema import (
    CamperPathologicalBackCreate,
    CamperPathologicalBackModify,
)


def get_all_camper_pathological_background(db: Session):
    rows = db.query(CamperPathologicalBackground).all()
    return rows


def get_all_camper_pathological_background_id_name(db: Session):
    rows = db.query(
        CamperPathologicalBackground.id, CamperPathologicalBackground.name
    ).all()
    return db_mapping_rows_to_dict(rows)


def get_camper_pathological_background_by_uuid(
    db: Session, camper_pathological_background_id: int
):
    return (
        db.query(CamperPathologicalBackground)
        .filter_by(
            id=camper_pathological_background_id,
        )
        .first()
    )


def create_new_camper_pathological_background(
    db: Session, new_camper_pathological_background: CamperPathologicalBackCreate
):
    db_camper_pathological_background = None
    try:
        db_camper_pathological_background = CamperPathologicalBackground(
            id=new_camper_pathological_background.id,
            camper_id=new_camper_pathological_background.camper_id,
            pathological_background_id=new_camper_pathological_background.pathological_background_id,
            is_active=new_camper_pathological_background.is_active,
        )
        db.add(db_camper_pathological_background)
        db.commit()
        db.refresh(db_camper_pathological_background)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_pathological_background = None
        return db_camper_pathological_background
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_pathological_background


def update_camper_pathological_background_by_ids(
    db: Session,
    camper_pathological_background_id: int,
    camper_id:int,
    modify_camper_pathological_background: CamperPathologicalBackModify,
):
    rows_updated = (
        db.query(CamperPathologicalBackground)
        .filter_by(pathological_background_id=camper_pathological_background_id, camper_id=camper_id)
        .update(modify_camper_pathological_background, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
