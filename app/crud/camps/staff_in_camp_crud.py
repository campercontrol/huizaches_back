from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import StaffInCamp, Camp, Location
from model.catalogs import Constant
from schema.camps.staff_in_camp_schema import (
    StaffInCampCreate,
    StaffInCampModify,
)


def get_all_staff_in_camp(db: Session):
    rows = db.query(StaffInCamp).all()
    return rows


def create_new_staff_in_camp(db: Session, new_staff_in_camp: StaffInCampCreate):
    db_staff_in_camp = None
    try:
        db_staff_in_camp = StaffInCamp(**new_staff_in_camp.dict())
        db.add(db_staff_in_camp)
        db.commit()
        db.refresh(db_staff_in_camp)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_staff_in_camp = None
        return db_staff_in_camp
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_staff_in_camp


def volunteer_staff(db: Session, new_staff_in_camp: StaffInCampCreate):
    db_staff_in_camp = None
    try:
        db_staff_in_camp = StaffInCamp(**new_staff_in_camp.dict())
        db_staff_in_camp.confirmed_staff= False
        db.add(db_staff_in_camp)
        db.commit()
        db.refresh(db_staff_in_camp)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_staff_in_camp = None
        return db_staff_in_camp
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_staff_in_camp

#def assign_staff(db: Session, staff_id:int, camp_id:int):

def unsubscribe_staff(db:Session, id_staff_in_camp: int):
    db.query(StaffInCamp).filter_by(id=id_staff_in_camp).delete()
    db.commit()
    return