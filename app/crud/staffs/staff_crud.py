from sqlalchemy import case, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.staffs import Staff
from model.camps import StaffInCamp, Camp, Location, Season
from model import User

from schema.staffs.staff_schema import ProspectCreate


def get_all_prospect(db):
    rows = (
        db.query(Staff, User.email, Season.name.label("season_name"))
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .filter(Staff.employee==False)        
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def create_new_prospect(db, new_prospect: ProspectCreate, user_id: int):
    db_prospect = None
    try:
        new_prospect.login_id = user_id
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


def delete_prospect(db, prospect_id: int):
    prospect = db.query(Staff).filter(Staff.id == prospect_id).first()
    db.delete(prospect)
    db.commit()
    return {"ok": True}


def accept_prospect(db, prospect_id: int):
    prospect = db.query(Staff).filter_by(id=prospect_id).update({"employee": True})
    db.commit()
    return {"message: Prospecto aceptado como staff"}


def staff_dashboard(db, staff_id: int):
    available_camps = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Location.name.label("location_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end")
        )
        .join(StaffInCamp, StaffInCamp.camp_id == Camp.id )
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                StaffInCamp.staff_id == staff_id,
                StaffInCamp.confirmed_staff == False,
                Camp.active == True,
                Camp.end >= date.today()
            )
        )
        .all()
    )

    available_camps = db_mapping_rows_to_dict(available_camps)

    staff_camps = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Location.name.label("location_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end")
        )
        .join(StaffInCamp, StaffInCamp.camp_id == Camp.id )
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                StaffInCamp.staff_id == staff_id,
                StaffInCamp.confirmed_staff == True,
                Camp.active == True,
                Camp.end >= date.today()
            )
        )
        .all()
    )
    
    staff_camps = db_mapping_rows_to_dict(staff_camps)

    next_camps = (
        db.query(
            Camp.id.label("camp_id"),        
            Camp.name.label("camp_name"),
            Location.name.label("location_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"))
        .join(Location, Location.id == Camp.location_id)
        .filter(
            and_(
                Camp.active == True,
                Camp.end >= date.today(),
            )
        )
        .all()
    )

    next_camps = db_mapping_rows_to_dict(next_camps)

    return {
        "available_camps": available_camps,
        "staff_camps": staff_camps,
        "next_camps": next_camps,
    }
