from sqlalchemy import func, select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.staffs import StaffRecord,Staff
from model.camps.staff_in_camp import StaffInCamp
from model.camps.camp import Camp

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
        db.query(StaffRecord.id, StaffRecord.attend, StaffRecord.attended, StaffRecord.total).select_from(StaffRecord)
        .join(Staff, StaffRecord.id == Staff.record_id)
        .filter(Staff.id == staff_id)
        .first()
    )
    
    
    return record_numbers

def get_staff_past_camps(db: Session, staff_id):
    query = (db.query(func.count()).select_from(StaffInCamp).join(Camp, StaffInCamp.camp_id == Camp.id)
             .where(and_(StaffInCamp.staff_id == staff_id, Camp.start < func.current_date())))
    data = db.execute(query).scalar()
    return data

def get_staff_upcoming_camps(db: Session, staff_id):
    query = (db.query(func.count()).select_from(StaffInCamp).join(Camp, StaffInCamp.camp_id == Camp.id)
             .where(and_(StaffInCamp.staff_id == staff_id, Camp.start > func.current_date())))
    data = db.execute(query).scalar()
    return data

def update_all_staff_record_status(db: Session):
    staffs = (db.query(Staff.id, StaffRecord.id.label("record_id")).select_from(Staff).join(StaffRecord, StaffRecord.id == Staff.record_id).all())
    try: 
        for staff in staffs:
            past_camps = get_staff_past_camps(db, staff.id)
            past_camps = get_staff_past_camps(db, staff.id)
            new_staff_record = get_staff_record_by_id(db, staff.record_id)
            upcoming_camps = get_staff_upcoming_camps(db, staff.id)
            total = upcoming_camps + past_camps
            new_staff_record.attend = upcoming_camps
            new_staff_record.attended = past_camps
            new_staff_record.total = total
            db.add(new_staff_record)
        db.commit()
    except Exception as ex:
        db.rollback()
        print(f"an error ocurred while saving {ex}")
        return False
    return True

def update_staff_record_status(db: Session, staff_id):
    staff = (db.query(Staff.id, StaffRecord.id.label("record_id")).select_from(Staff).join(StaffRecord, StaffRecord.id == Staff.record_id).filter(Staff.id == staff_id).first())
    try: 
        past_camps = get_staff_past_camps(db, staff.id)
        past_camps = get_staff_past_camps(db, staff.id)
        new_staff_record = get_staff_record_by_id(db, staff.record_id)
        upcoming_camps = get_staff_upcoming_camps(db, staff.id)
        total = upcoming_camps + past_camps
        new_staff_record.attend = upcoming_camps
        new_staff_record.attended = past_camps
        new_staff_record.total = total
        db.add(new_staff_record)
        db.commit()
    except Exception as ex:
        db.rollback()
        print(f"an error ocurred while saving {ex}")
        return False
    return True
