from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.staffs import StaffRecord

from schema.staffs.staff_record_schema import (
    StaffRecordCreate,
    StaffRecordModify,
)


def get_all_staff_record(db):
    rows = db.query(StaffRecord).all()
    return rows


def get_staff_record_by_id(db, staff_record_id: int):
    return (
        db.query(StaffRecord)
        .filter_by(
            id=staff_record_id,
        )
        .first()
    )


def create_new_staff_record(db, new_staff_record: StaffRecordCreate):
    db_staff_record = None
    try:
        db_staff_record = StaffRecord(**new_staff_record.dict())
        db.add(db_staff_record)
        db.commit()
        db.refresh(db_staff_record)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_staff_record = None
        return db_staff_record
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_staff_record


def update_staff_record_by_id(db, staff_record_id: int, modify_staff_record: StaffRecordModify):
    rows_updated = (
        db.query(StaffRecord)
        .filter_by(id=staff_record_id)
        .update(modify_staff_record, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_record_by_staff_id(db, staff_id:int):
    
    record_numbers = (
        db.query(StaffRecord.attend, StaffRecord.attended, StaffRecord.total)
        .filter_by(staff_id=staff_id)
        .first()
    )
    
    return record_numbers