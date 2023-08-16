from sqlalchemy import case, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.staffs import Staff
from model.camps import StaffInCamp, Camp, Location, Season
from model import User

from schema.staffs.staff_schema import ProspectCreate, StaffModify
from crud.camps.camp_crud import get_records_for_camp




def get_all_prospect(db):
    rows = (
        db.query(Staff, User.email, Season.name.label("season_name"))
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .filter(Staff.employee==False)        
        .all()
    )
    return db_mapping_rows_to_dict(rows)

def get_all_staff(db):
    rows = (
        db.query(Staff, User.email, Season.name.label("season_name"))
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .filter(Staff.employee==True)        
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def create_new_prospect(db, new_prospect: ProspectCreate, user_id: int):
    db_prospect = None
    try:
        new_prospect.login_id = user_id
        db_prospect = Staff(**new_prospect.dict())
        db_prospect.employee = False
        db_prospect.coordinator = False
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
    user_id = db.query(Staff.login_id).filter_by(id=prospect_id).first()
    user = db.query(User).filter_by(id=user_id[0]).update({"is_employee": True})
    db.commit()
    return {"message: Prospecto aceptado como staff"}

def update_staff_by_id(
    db: Session, staff_id: int, modify_staff: StaffModify
    ) -> any:
    rows_updated = (
        db.query(Staff)
        .filter_by(id=staff_id)
        .update(modify_staff, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def staff_dashboard(db, staff_id: int):



    user =  (db.query(User.is_active, User.is_employee, Staff.staff_contact_name)
            .join(User, User.id == Staff.login_id)
            .filter(Staff.id == staff_id)
            .first()            
            )
    
    print("#############################")
    print(user)

    if user[0] and user[1] and user[2]:


        camps_id = []
        available_camps = (
            db.query(
                StaffInCamp.id.label("staff_in_camp_id"),
                Camp.id.label("camp_id"),
                Camp.name.label("camp_name"),
                Location.name.label("location_name"),
                Camp.public_price.label ("public_price") ,
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
        available_camps_final = []

        for staff_in_camp in available_camps: 
            camps_id.append(staff_in_camp["camp_id"])
            records = get_records_for_camp(db, staff_in_camp['camp_id'])
            staff_in_camp = dict(staff_in_camp)
            staff_in_camp['records'] = records
            available_camps_final.append(staff_in_camp)

        staff_camps = (
            db.query(
                StaffInCamp.id.label("staff_in_camp_id"),
                Camp.id.label("camp_id"),
                Camp.name.label("camp_name"),
                Location.name.label("location_name"),
                Camp.public_price.label ("public_price") ,
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
        staff_camps_final = []

        for staff_in_camp in staff_camps: 
            camps_id.append(staff_in_camp["camp_id"])
            records = get_records_for_camp(db, staff_in_camp['camp_id'])
            staff_in_camp = dict(staff_in_camp)
            staff_in_camp['records'] = records
            staff_camps_final.append(staff_in_camp)

        next_camps = (
            db.query(
                Camp.id.label("camp_id"),        
                Camp.name.label("camp_name"),
                Location.name.label("location_name"),
                Camp.public_price.label ("public_price") ,
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
        next_camps_filter  = [d for d in next_camps if d['camp_id'] not in  camps_id]
        next_camps_final = []

        for camp in next_camps_filter:
            records = get_records_for_camp(db, camp['camp_id'])
            camp = dict(camp)
            camp['records'] = records
            next_camps_final.append(camp)

        return {
            "available_camps": available_camps_final,
            "staff_camps": staff_camps_final,
            "next_camps": next_camps_final,
        }
    
    else: 
        complete_profile = True if user[2] else False
        return {"is_active": user[0],
                "is_employee": user[1],
                "complete_profile": complete_profile
                } 

def get_staff_by_id(db, staff_id:int):
    staff = (
        db.query(Staff)
        .filter_by(id=staff_id)
        .first()
    )
    return staff