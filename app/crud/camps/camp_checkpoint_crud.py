from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import CampCheckpoint
from model.camps import Camp, Location

from schema.camps.camp_checkpoint_schema import (
    CampCheckpointCreate,
    CampCheckpointModify,
)


def get_all_camp_checkpoint(db):
    rows = db.query(CampCheckpoint).all()
    return rows


def get_camp_checkpoint_by_id(db, camp_checkpoint_id: int):
    return (
        db.query(CampCheckpoint)
        .filter_by(
            id=camp_checkpoint_id,
        )
        .first()
    )


def create_new_camp_checkpoint(db, new_camp_checkpoint: CampCheckpointCreate):
    db_camp_checkpoint = None
    try:
        db_camp_checkpoint = CampCheckpoint(**new_camp_checkpoint.dict())
        db.add(db_camp_checkpoint)
        db.commit()
        db.refresh(db_camp_checkpoint)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camp_checkpoint = None
        return db_camp_checkpoint
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camp_checkpoint


def update_camp_checkpoint_by_id(db, camp_checkpoint_id: int, modify_camp_checkpoint: CampCheckpointModify):
    rows_updated = (
        db.query(CampCheckpoint)
        .filter_by(id=camp_checkpoint_id)
        .update(modify_camp_checkpoint, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_camp_checkpoint_by_camp(db, camp_id: int):
    rows = (
        db.query(CampCheckpoint)
        .join(Camp, Camp.id == camp_id)
        .filter_by(camp_id = camp_id)
        .all()
    )
    return rows


def get_camps_with_checkpoint(db):
    camps_id = []
    camp_checkpoints = get_all_camp_checkpoint(db)
    for camp_checkpoint in camp_checkpoints:
        if getattr(camp_checkpoint, "camp_id") not in camps_id:
            camps_id.append(getattr(camp_checkpoint, "camp_id"))
             
    rows = (
        db.query(Camp.id, Camp.name, Camp.start, Camp.end, Location.name)
        .join(Location, Camp.location_id == Location.id)
        .filter(Camp.id.in_(camps_id))
        .all()
    )
    return db_mapping_rows_to_dict(rows)

def delete_camp_checkpoint(db, camp_checkpoint_id:int):
    camp_checkpoint = db.query(CampCheckpoint).filter(CampCheckpoint.id==camp_checkpoint_id).first()
    db.delete(camp_checkpoint)
    db.commit()
    return {"status" : True}
