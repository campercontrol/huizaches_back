from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.campers import CamperRecord

from schema.campers.camper_record_schema import (
    CamperRecordCreate,
    CamperRecordModify,
)


def get_all_camper_record(db):
    rows = db.query(CamperRecord).all()
    return rows


def get_camper_record_by_id(db, camper_record_id: int):
    return (
        db.query(CamperRecord)
        .filter_by(
            id=camper_record_id,
        )
        .first()
    )


def create_new_camper_record(db, new_camper_record: CamperRecordCreate):
    db_camper_record = None
    try:
        db_camper_record = CamperRecord(**new_camper_record.dict())
        db.add(db_camper_record)
        db.commit()
        db.refresh(db_camper_record)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_record = None
        return db_camper_record
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_record


def update_camper_record_by_id(db, camper_record_id: int, modify_camper_record: CamperRecordModify):
    rows_updated = (
        db.query(CamperRecord)
        .filter(CamperRecord.id==camper_record_id)
        .update(modify_camper_record, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_record_by_camper_id(db, camper_id:int):
    
    record_numbers = (
        db.query(CamperRecord.attend, CamperRecord.attended, CamperRecord.total)
        .filter_by(camper_id=camper_id)
        .first()
    )
    
    return record_numbers