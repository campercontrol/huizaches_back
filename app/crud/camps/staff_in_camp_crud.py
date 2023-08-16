from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import StaffInCamp, Camp, Location
from model.staffs import Staff, StaffRecord
from model.catalogs import Constant, StaffRole
from model.user import User
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
        db_staff_in_camp.confirmed_staff = False
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


# def assign_staff(db: Session, staff_id:int, camp_id:int):


def unsubscribe_staff(db: Session, id_staff_in_camp: int):
    db.query(StaffInCamp).filter_by(id=id_staff_in_camp).delete()
    db.commit()
    return


def get_staff_volunteer_in_camp(db: Session, camp_id: int):
    staff_volunteer = (
        db.query(
            Staff.id.label("staff_id"),
            Staff.photo.label("staff_photo"),
            (
                Staff.name + " " + Staff.lastname_father + " " + Staff.lastname_mother
            ).label("staff_full_name"),
            Staff.birthday.label("staff_birthday"),
            Staff.cellphone.label("staff_cellphone"),
            User.email.label("staff_email"),
            StaffInCamp.updated_at.label("staff_volunteer_date"),
            StaffRecord.attend.label("staff_attend"),
            StaffRecord.attended.label("staff_attended"),
            StaffRecord.total.label("staff_total"),
        )
        .join(Staff, Staff.id == StaffInCamp.staff_id)
        .outerjoin(StaffRecord, StaffRecord.id == Staff.record_id)
        .join(User, User.id == Staff.login_id)
        .filter(StaffInCamp.camp_id == camp_id, StaffInCamp.confirmed_staff == False)
        .all()
    )
    return db_mapping_rows_to_dict(staff_volunteer)


def get_staff_in_camp(db: Session, camp_id: int):
    staff = (
        db.query(
            Staff.id.label("staff_id"),
            Staff.photo.label("staff_photo"),
            (
                Staff.name + " " + Staff.lastname_father + " " + Staff.lastname_mother
            ).label("staff_full_name"),
            Staff.birthday.label("staff_birthday"),
            Staff.cellphone.label("staff_cellphone"),
            User.email.label("staff_email"),
            StaffRecord.attend.label("staff_attend"),
            StaffRecord.attended.label("staff_attended"),
            StaffRecord.total.label("staff_total"),
            StaffRole.name.label("staff_role"),
        )
        .select_from(StaffInCamp)
        .join(Staff, Staff.id == StaffInCamp.staff_id)
        .outerjoin(StaffRecord, StaffRecord.id == Staff.record_id)
        .join(User, User.id == Staff.login_id)
        .outerjoin(StaffRole, StaffRole.id == StaffInCamp.assigned_role_id)
        .filter(StaffInCamp.camp_id == camp_id, StaffInCamp.confirmed_staff == True)
        .all()
    )

    return db_mapping_rows_to_dict(staff)


def accept_staff_in_camp(db: Session, camp_id: int, staffs_id: list[int]):
    for staff_id in staffs_id:
        staff_in_camp = (
            db.query(StaffInCamp)
            .filter(
                and_(StaffInCamp.camp_id == camp_id, StaffInCamp.staff_id == staff_id)
            )
            .all()
        )

        if staff_in_camp:
            db.query(StaffInCamp).filter(
                and_(StaffInCamp.camp_id == camp_id, StaffInCamp.staff_id == staff_id)
            ).update({"confirmed_staff": True})
            db.commit()
        else:
            new_staff_in_camp = StaffInCampCreate(
                confirmed_staff = True ,
                camp_id = camp_id,
                staff_id = staff_id,
            )
            create_new_staff_in_camp(db, new_staff_in_camp)

    return "Success"


def assign_role_staff(db: Session, camp_id:int, staffs_id: list[int], role_id:int):
    
    for staff_id in staffs_id:
        staff_in_camp = (
            db.query(StaffInCamp)
            .filter(
                and_(StaffInCamp.camp_id == camp_id, StaffInCamp.staff_id == staff_id)
            )
            .update({"assigned_role_id": role_id})
        )
        db.commit()
    return "Success"
