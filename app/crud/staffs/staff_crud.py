from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.staffs import Staff
from model import User

from schema.staffs.staff_schema import ProspectCreate


def get_all_prospect(db):
    rows = (
        db.query(Staff)
        .join(User, User.id == Staff.login_id)
        .filter(and_(User.active == True, Staff.employee == False))
        .all()
    )
    return rows


def create_new_prospect(db, new_prospect: ProspectCreate):
    db_prospect = None
    try:
        db_prospect = Staff(**new_prospect.dict())
        db_prospect.employee = False
        db.add(db_prospect)
        db.commit()
        db.refresh(db_prospect)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_prospect = None
        return db_prospect
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_prospect

