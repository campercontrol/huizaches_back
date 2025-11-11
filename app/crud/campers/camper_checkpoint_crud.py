from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.campers import CamperCheckpoint
from model.campers import Camper

from schema.campers.camper_checkpoint_schema import (
    CamperCheckpointCreate,
    CamperCheckpointModify,
)


def get_all_camper_checkpoint(db):
    rows = db.query(CamperCheckpoint).all()
    return rows


def get_camper_checkpoint_by_id(db, camper_checkpoint_id: int):
    return (
        db.query(CamperCheckpoint)
        .filter_by(
            id=camper_checkpoint_id,
        )
        .first()
    )


def create_new_camper_checkpoint(db, new_camper_checkpoint: CamperCheckpointCreate):
    db_camper_checkpoint = None
    try:
        db_camper_checkpoint = CamperCheckpoint(**new_camper_checkpoint.dict())
        db.add(db_camper_checkpoint)
        db.commit()
        db.refresh(db_camper_checkpoint)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_checkpoint = None
        return db_camper_checkpoint
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_checkpoint


def update_camper_checkpoint_by_id(db, camper_checkpoint_id: int, modify_camper_checkpoint: CamperCheckpointModify):
    rows_updated = (
        db.query(CamperCheckpoint)
        .filter_by(id=camper_checkpoint_id)
        .update(modify_camper_checkpoint, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_camper_checkpoint_by_camper(db, camper_id: int):
    rows = (
        db.query(CamperCheckpoint)
        .join(Camper, Camper.id == camper_id)
        .filter(CamperCheckpoint.camper_id == camper_id)
        .all()
    )
    return rows


def get_camper_checkpoint_by_camper_check_id(db, camper_id: int, checkpoint_id:int):
    rows = (
        db.query(CamperCheckpoint.id,
                 CamperCheckpoint.checkin,
                 CamperCheckpoint.checkin_date,
                 CamperCheckpoint.camper_id,
                 CamperCheckpoint.checkpoint_id,
                 CamperCheckpoint.created_at,
                 CamperCheckpoint.updated_at
        )
        .join(Camper, Camper.id == camper_id)
        .filter(and_(CamperCheckpoint.camper_id == camper_id, CamperCheckpoint.checkpoint_id == checkpoint_id))
        .first()
    )
    return rows