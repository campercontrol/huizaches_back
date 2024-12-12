from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import date
from model.campers import School
from model.camps import Camp
from model.camps.season import Season
from model.camps.location import Location
from crud.crud_user import create_new_user_admin, get_user_by_email
from crud.camps.camp_crud import get_records_for_camp
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case
from model.user import User
from utils.hash import hash_str
from schema.user import UserCreate
from schema.campers.school_schema import UpdateSchool

def get_all_school(db):
    rows= db.query(School).all()
    return rows

def get_upcoming_school_camps(db: Session, school_id: int):
    query = (
                db.query(
                    Camp.id,
                     Camp.name,
                     Camp.start,
                     Camp.end,
                     Camp.start_registration,
                     Camp.end_registration,
                     Camp.registration,
                     Camp.url,
                     Camp.special_message,
                     Camp.special_message_admin,
                     Camp.public_price,
                     Camp.show_payment_parent,
                     Camp.show_rebate_parent,
                     Camp.show_paypal_button,
                     Camp.show_payment_order,
                     Camp.reminder_camp_days,
                     Camp.reminder_discount_days,                                                        
                     Camp.insurance,
                     Camp.venue,
                     Camp.photo_url,
                     Camp.photo_password,
                     Camp.medical_report,
                     Camp.occupancy_camp,
                     Camp.active,
                     Camp.general_camp,
                     School.name.label("school"),
                     Location.name.label("location"),
                     Season.name.label("season_name"),
                     Camp.show_mercadopago_button,
                     Camp.recommended_payment_dates
                    )
                .join(Location, Camp.location_id == Location.id)
                .join(School, School.id == Camp.school_id)
                .join(Season, Camp.season_id == Season.id)
                .where(and_(Camp.school_id == school_id, Camp.start > date.today()))
            )
    camps = []            
    camps_data = db.execute(query)
    camps_data = camps_data.mappings().all()
    for camp in camps_data:
        camp = dict(camp)
        camp["records"] = get_records_for_camp(db, camp["id"])
        camps.append(camp)
    return camps
    
def get_past_school_camps(db: Session, school_id: int):
    query = (
                db.query(
                    Camp.id,
                     Camp.name,
                     Camp.start,
                     Camp.end,
                     Camp.start_registration,
                     Camp.end_registration,
                     Camp.registration,
                     Camp.url,
                     Camp.special_message,
                     Camp.special_message_admin,
                     Camp.public_price,
                     Camp.show_payment_parent,
                     Camp.show_rebate_parent,
                     Camp.show_paypal_button,
                     Camp.show_payment_order,
                     Camp.reminder_camp_days,
                     Camp.reminder_discount_days,                                                        
                     Camp.insurance,
                     Camp.venue,
                     Camp.photo_url,
                     Camp.photo_password,
                     Camp.medical_report,
                     Camp.occupancy_camp,
                     Camp.active,
                     Camp.general_camp,
                     School.name.label("school"),
                     Location.name.label("location"),
                     Season.name.label("season_name"),
                     Camp.show_mercadopago_button,
                     Camp.recommended_payment_dates
                    )
                .join(Location, Camp.location_id == Location.id)
                .join(School, School.id == Camp.school_id)
                .join(Season, Camp.season_id == Season.id)
                .where(and_(Camp.school_id == school_id, Camp.start < date.today()))
            )
    camps = []            
    camps_data = db.execute(query)
    camps_data = camps_data.mappings().all()
    for camp in camps_data:
        camp = dict(camp)
        camp["records"] = get_records_for_camp(db, camp["id"])
        camps.append(camp)
    return camps
    

def get_school_by_uuid(db, school_id):
    return(
        db.query(School)
        .filter_by(
            id=school_id
        )
        .first()
    )

def create_new_school(db, new_school):
    try:        
        user_exist = get_user_by_email(db, new_school.login_email)
        
        if user_exist:
            return 2
        
        new_user_obj = UserCreate(
            email=new_school.login_email,
            passw=new_school.password,
            role_id=3,
            is_superuser=False,
            is_coordinator=False,
            is_employee=False,
            is_admin=False,
        )
        new_school_user = create_new_user_admin(db, new_user_obj)
        db_school = School(
                id=new_school.id,
                login_id=new_school_user.id,
                name=new_school.name,
                address = new_school.address,
                url = new_school.url,
                contact = new_school.contact,
                phone = new_school.phone,
                cellphone = new_school.cellphone,
                email = new_school.contact_first_email,
                contact_second_name = new_school.contact_second_name,
                contact_second_phone = new_school.contact_second_phone,
                contact_second_cellphone = new_school.contact_second_cellphone,
                contact_second_email = new_school.contact_second_email,
                contact_third_name = new_school.contact_third_name,
                contact_third_phone = new_school.contact_third_phone,
                contact_third_cellphone = new_school.contact_third_cellphone,
                contact_third_email = new_school.contact_third_email,
                verify = new_school.verify,
                active = new_school.active,
                created_at = new_school.created_at 
        )
        db.add(db_school)
        db.commit()
        return 1
    except Exception as ex:
        db.rollback()
        print(f"An error ocurred while creating school{ex}")
        return 3



def update_school_controller(db: Session, school_id: int, modify_school: UpdateSchool):
    try:
        new_school = modify_school.school.dict()
        db_school = db.query(School).filter_by(id=school_id).update(new_school, synchronize_session="fetch")
        if modify_school.password != '' and modify_school.password is not None:
            new_hashed_password = hash_str(modify_school.password) 
            db_user = db.query(User).filter(User.id == new_school['login_id']).first()
            db_user.hashed_pass = new_hashed_password
        db.commit()
        return 1
    except Exception as ex:
        db.rollback()
        print(ex)
        return 3


def get_active_school(db):
    rows= db.query(School.id, School.name).filter_by(active=True).all()
    return db_mapping_rows_to_dict(rows)

def delete_school(db: Session, school_id:int):
    school = db.query(School).filter(School.id==school_id).first()
    db.delete(school)
    db.commit()
    return {"status" : True}

def school_dashboard(db: Session, school_id: int):
    pass
    # user = (
    #     db.query(User.is_active, User.is_employee, Staff.staff_contact_name)
    #     .join(User, User.id == Staff.login_id)
    #     .filter(Staff.id == staff_id)
    #     .first()
    # )

    # if user[0] and user[1] and user[2]:
    #     camps_id = []
    #     available_camps = (
    #         db.query(
    #             StaffInCamp.id.label("staff_in_camp_id"),
    #             Camp.id.label("camp_id"),
    #             Camp.name.label("camp_name"),
    #             Location.name.label("location_name"),
    #             Camp.public_price.label("public_price"),
    #             Camp.start.label("camp_start"),
    #             Camp.end.label("camp_end"),
    #         )
    #         .join(StaffInCamp, StaffInCamp.camp_id == Camp.id)
    #         .join(Location, Camp.location_id == Location.id)
    #         .filter(
    #             and_(
    #                 StaffInCamp.staff_id == staff_id,
    #                 StaffInCamp.confirmed_staff == False,
    #                 Camp.active == True,
    #                 Camp.end >= date.today(),
    #             )
    #         )
    #         .all()
    #     )
    #     available_camps = db_mapping_rows_to_dict(available_camps)
    #     available_camps_final = []

    #     for staff_in_camp in available_camps:
    #         camps_id.append(staff_in_camp["camp_id"])
    #         records = get_records_for_camp(db, staff_in_camp["camp_id"])
    #         staff_in_camp = dict(staff_in_camp)
    #         staff_in_camp["records"] = records
    #         available_camps_final.append(staff_in_camp)

    #     staff_camps = (
    #         db.query(
    #             StaffInCamp.id.label("staff_in_camp_id"),
    #             Camp.id.label("camp_id"),
    #             Camp.name.label("camp_name"),
    #             Location.name.label("location_name"),
    #             Camp.public_price.label("public_price"),
    #             Camp.start.label("camp_start"),
    #             Camp.end.label("camp_end"),
    #         )
    #         .join(StaffInCamp, StaffInCamp.camp_id == Camp.id)
    #         .join(Location, Camp.location_id == Location.id)
    #         .filter(
    #             and_(
    #                 StaffInCamp.staff_id == staff_id,
    #                 StaffInCamp.confirmed_staff == True,
    #                 Camp.active == True,
    #                 Camp.end >= date.today(),
    #             )
    #         )
    #         .all()
    #     )

    #     staff_camps = db_mapping_rows_to_dict(staff_camps)
    #     staff_camps_final = []

    #     for staff_in_camp in staff_camps:
    #         camps_id.append(staff_in_camp["camp_id"])
    #         records = get_records_for_camp(db, staff_in_camp["camp_id"])
    #         staff_in_camp = dict(staff_in_camp)
    #         staff_in_camp["records"] = records
    #         staff_camps_final.append(staff_in_camp)

    #     next_camps = (
    #         db.query(
    #             Camp.id.label("camp_id"),
    #             Camp.name.label("camp_name"),
    #             Location.name.label("location_name"),
    #             Camp.public_price.label("public_price"),
    #             Camp.start.label("camp_start"),
    #             Camp.end.label("camp_end"),
    #         )
    #         .join(Location, Location.id == Camp.location_id)
    #         .filter(
    #             and_(
    #                 Camp.active == True,
    #                 Camp.end >= date.today(),
    #             )
    #         )
    #         .all()
    #     )

    #     next_camps = db_mapping_rows_to_dict(next_camps)
    #     next_camps_filter = [d for d in next_camps if d["camp_id"] not in camps_id]
    #     next_camps_final = []

    #     for camp in next_camps_filter:
    #         records = get_records_for_camp(db, camp["camp_id"])
    #         camp = dict(camp)
    #         camp["records"] = records
    #         next_camps_final.append(camp)

    #     return {
    #         "available_camps": available_camps_final,
    #         "staff_camps": staff_camps_final,
    #         "next_camps": next_camps_final,
    #     }

    # else:
    #     complete_profile = True if user[2] else False
    #     return {
    #         "is_active": user[0],
    #         "is_employee": user[1],
    #         "complete_profile": complete_profile,
    #     }
