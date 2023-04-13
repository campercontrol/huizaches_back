from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.campers import CamperPathologicalBackgroundFamily
from schema.campers_catalogs.camper_pathological_background_fm_schema import (
    CamperPathologicalBackFmCreate,
    CamperPathologicalBackFmModify,
)


def get_all_camper_pathological_background_fm(db: Session):
    rows = db.query(CamperPathologicalBackgroundFamily).all()
    return rows


def get_all_camper_pathological_background_fm_id_name(db: Session):
    rows = db.query(
        CamperPathologicalBackgroundFamily.id, CamperPathologicalBackgroundFamily.name
    ).all()
    return db_mapping_rows_to_dict(rows)


def get_camper_pathological_background_fm_by_uuid(
    db: Session, camper_pathological_background_fm_id: int
):
    return (
        db.query(CamperPathologicalBackgroundFamily)
        .filter_by(
            id=camper_pathological_background_fm_id,
        )
        .first()
    )


def create_new_camper_pathological_background_fm(
    db: Session, new_camper_pathological_background_fm: CamperPathologicalBackFmCreate
):
    db_camper_pathological_background_fm = None
    try:
        db_camper_pathological_background_fm = CamperPathologicalBackgroundFamily(
            id=new_camper_pathological_background_fm.id,
            camper_id=new_camper_pathological_background_fm.camper_id,
            pathological_background_family_id=new_camper_pathological_background_fm.pathological_background_fm_id,
            is_active=new_camper_pathological_background_fm.is_active,
        )
        db.add(db_camper_pathological_background_fm)
        db.commit()
        db.refresh(db_camper_pathological_background_fm)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_pathological_background_fm = None
        return db_camper_pathological_background_fm
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_pathological_background_fm


def update_camper_pathological_background_fm_by_ids(
    db: Session,
    camper_pathological_background_fm_id: int,
    camper_id:int,
    modify_camper_pathological_background_fm: CamperPathologicalBackFmModify,
):
    rows_updated = (
        db.query(CamperPathologicalBackgroundFamily)
        .filter_by(pathological_background_family_id=camper_pathological_background_fm_id, camper_id=camper_id)
        .update(modify_camper_pathological_background_fm, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
