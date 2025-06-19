from fastapi import HTTPException
from sqlalchemy import case, and_, or_, desc, asc, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from utils.hash import hash_str
from datetime import date
from model.staffs import Staff, StaffRecord
from model.camps import StaffInCamp, Camp, Location, Season
from model.staffs.staff_food_restriction import StaffFoodRestriction
from model.staffs.staff_vaccine import StaffVaccine
from model import User
from model.catalogs.food_restriction import FoodRestriction
from model.catalogs.vaccine import Vaccine
from schema.staff_catalogs.staff_food_restriction_schema import StaffFoodRestrictionCreate
from schema.staff_catalogs.staff_vaccine_schema import StaffVaccineCreate
from schema.pagination.pagination_schema import Pagination, SortEnum
from schema.staffs.staff_schema import ProspectCreate, StaffModify
from crud.camps.camp_crud import get_records_for_camp
from crud.camps.season_crud import get_current_Season
from crud.mailings.mailing_crud import get_admin_users_for_mailing
from crud.catalogs.vaccine_crud import get_all_vaccine
from crud.catalogs.food_restriction_crud import get_all_food_restriction
from helper.pagination_helpers import pagination_params, get_number_of_pages
from helper.mailing_helpers import send_mail_template
from utils.functions_jwt import create_user_verification_url


def get_all_prospect(db, pagination):
    order = desc if pagination.order == SortEnum.DESC else asc
    query = (
        db.query(Staff, User.email, Season.name.label("season_name"),
                    StaffRecord.attend,
                    StaffRecord.attended,
                    StaffRecord.total)
        .select_from(Staff)
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .join(StaffRecord, StaffRecord.id == Staff.record_id)
        .filter(Staff.employee == False)
        .order_by(order(Staff.name))
        .limit(pagination.perPage)
        .offset((pagination.offset))
    )
    data = db.execute(query)
    data = data.mappings().all()
    rows_count = (
        db.query(func.count(Staff.id))
        .select_from(Staff)
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .join(StaffRecord, StaffRecord.id == Staff.record_id)
        .filter(Staff.employee == False).scalar()        
    )
    pages = get_number_of_pages(rows_count, pagination.perPage)

    return {
        "pages": pages,
        "items": data,
        "total": rows_count
        }

def search_all_prospect(db, pagination: Pagination, name: str, email: str):
    query = (
        db.query(Staff, User.email, Season.name.label("season_name"),
                    StaffRecord.attend,
                    StaffRecord.attended,
                    StaffRecord.total)
        .select_from(Staff)
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .join(StaffRecord, StaffRecord.id == Staff.record_id)
        .filter(Staff.employee == False)
        .filter(
            or_(
                User.email.op('%')(email),
                Staff.name.op('%')(name),
            )
        )
        .order_by(
            func.similarity(User.email, email).desc(),
            func.similarity(Staff.name, name).desc()
        )
        .limit(pagination.perPage)
        .offset((pagination.offset))
    )
    data = db.execute(query)
    data = data.mappings().all()
    rows_count = (
        db.query(func.count(Staff.id))
        .select_from(Staff)
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .join(StaffRecord, StaffRecord.id == Staff.record_id)
        .filter(Staff.employee == False)
        .filter(
            or_(
                User.email.op('%')(email),
                Staff.name.op('%')(name),
            )
        ).scalar()        
    )
    pages = get_number_of_pages(rows_count, pagination.perPage)

    return {
        "pages": pages,
        "items": data,
        "total": rows_count
        }


def get_all_prospect_by_season(db, season_id: int):
    rows = (
        db.query(
            Staff.id,
            (
                Staff.name + " " + Staff.lastname_father + " " + Staff.lastname_mother
            ).label("staff_fullname"),
            User.email.label("staff_email")
        )
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .filter(Staff.employee == False, Staff.season_id == season_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_all_staff(db, pagination):
    order = desc if pagination.order == SortEnum.DESC else asc
    query = (
        db.query(Staff, User.email, Season.name.label("season_name"),
                 StaffRecord.attend,
                 StaffRecord.attended,
                 StaffRecord.total)
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .join(StaffRecord, StaffRecord.id == Staff.record_id)
        .filter(Staff.employee == True)
        .order_by(order(Staff.name))
        .limit(pagination.perPage)
        .offset((pagination.offset))

    )
    data = db.execute(query)
    data = data.mappings().all()
    rows_count = (
        db.query(func.count(Staff.id))
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .join(StaffRecord, StaffRecord.id == Staff.record_id)
        .filter(Staff.employee == True).scalar()    
    )
    pages = get_number_of_pages(rows_count, pagination.perPage)

    return {
        "pages": pages,
        "items": data,
        "total": rows_count
        }
def search_all_staff(db, pagination: Pagination, name: str, email: str):
    query = (
        db.query(Staff, User.email, Season.name.label("season_name"),
                 StaffRecord.attend,
                 StaffRecord.attended,
                 StaffRecord.total)
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .join(StaffRecord, StaffRecord.id == Staff.record_id)
        .filter(Staff.employee == True)
        .filter(
           or_(
               User.email.op('%')(email),
               Staff.name.op('%')(name),
            )
        )
        .order_by(
            func.similarity(User.email, email).desc(),
            func.similarity(Staff.name, name).desc()
        )
        .limit(pagination.perPage)
        .offset((pagination.offset))

    )
    data = db.execute(query)
    data = data.mappings().all()
    rows_count = (
        db.query(func.count(Staff.id))
        .join(User, User.id == Staff.login_id)
        .join(Season, Staff.season_id == Season.id)
        .join(StaffRecord, StaffRecord.id == Staff.record_id)
        .filter(Staff.employee == True)
        .filter(
           or_(
               User.email.op('%')(email),
               Staff.name.op('%')(name),
            )
        )
        .scalar()    
    )
    pages = get_number_of_pages(rows_count, pagination.perPage)

    return {
        "pages": pages,
        "items": data,
        "total": rows_count
        }

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

def create_complete_prospect(db, new_prospect):
    
    try:
        season = get_current_Season(db)
        welcome_prospect_template = 1 
        admin_new_prospect_template = 1988
        vaccines = get_all_vaccine(db)
        all_food_restriction = get_all_food_restriction(db)
        
        user = db.query(User).filter_by(email=new_prospect.user.email).first()
        
        if user:
            return 2
    
        prospect_user = User(
            email= new_prospect.user.email,
            hashed_pass=hash_str(new_prospect.user.passw),
            role_id= 2,
            is_active= False,
            is_coordinator = False,
            is_admin = False,
            is_employee = False,
            is_superuser = False           
                 
        )
        db.add(prospect_user)
        db.flush()

        staff_new_record = StaffRecord(
            attend = 0,
            attended = 0,
            total = 0
        )
        db.add(staff_new_record)
        db.flush()

        new_prospect.prospect.login_id = prospect_user.id
        prospect_profile = Staff(**new_prospect.prospect.dict())
        prospect_profile.employee = False
        prospect_profile.coordinator = False
        prospect_profile.season_id = season['id']
        prospect_profile.record_id = staff_new_record.id    

        db.add(prospect_profile)
        db.flush()
        
        for vaccine in vaccines:
            staff_vaccine = StaffVaccine(
                staff_id = prospect_profile.id,
                vaccine_id = vaccine.id,
                is_active= False
            )
            db.add(staff_vaccine)
        
        for food_restriction in all_food_restriction:
            staff_food_restriction = StaffFoodRestriction(
                staff_id = prospect_profile.id,
                food_restriction_id = food_restriction.id,
                is_active= False
                 
            )            
            db.add(staff_food_restriction)

        db.commit()
        
        admin_users = get_admin_users_for_mailing(db)
    
        for admin_user in admin_users:
            admin_user_context = {
                "user": admin_user
            }   
            send_mail_template(db, admin_user['email'], admin_new_prospect_template, admin_user_context)
        verify_url = create_user_verification_url({"email": prospect_user.email})
        
        prospect_context = {
            "username": prospect_profile.name,
            "verify_url": verify_url
        }
        # send_mail_prospect(db, [prospect_user.email], welcome_prospect_template, prospect_profile, prospect_user)
        send_mail_template(db, [prospect_user.email], welcome_prospect_template, prospect_context)
        
               
        return 1
    except Exception as ex:
        db.rollback()      
        print(ex)
        return 3

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


def update_staff_by_id(db: Session, staff_id: int, modify_staff: StaffModify) -> any:
    rows_updated = (
        db.query(Staff)
        .filter_by(id=staff_id)
        .update(modify_staff, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def staff_camps(db, staff_id: int):
    pass

def staff_dashboard(db, staff_id: int):
    user = (
        db.query(User.is_active, User.is_employee, Staff.staff_contact_name)
        .join(User, User.id == Staff.login_id)
        .filter(Staff.id == staff_id)
        .first()
    )

    if user[0] and user[1] and user[2]:
        camps_id = []
        available_camps = (
            db.query(
                StaffInCamp.id.label("staff_in_camp_id"),
                Camp.id.label("camp_id"),
                Camp.name.label("camp_name"),
                Location.name.label("location_name"),
                Camp.public_price.label("public_price"),
                Camp.start.label("camp_start"),
                Camp.end.label("camp_end"),
            )
            .join(StaffInCamp, StaffInCamp.camp_id == Camp.id)
            .join(Location, Camp.location_id == Location.id)
            .filter(
                and_(
                    StaffInCamp.staff_id == staff_id,
                    StaffInCamp.confirmed_staff == False,
                    Camp.active == True,
                    Camp.end >= date.today(),
                )
            )
            .all()
        )
        available_camps = db_mapping_rows_to_dict(available_camps)
        available_camps_final = []

        for staff_in_camp in available_camps:
            camps_id.append(staff_in_camp["camp_id"])
            records = get_records_for_camp(db, staff_in_camp["camp_id"])
            staff_in_camp = dict(staff_in_camp)
            staff_in_camp["records"] = records
            available_camps_final.append(staff_in_camp)

        staff_camps = (
            db.query(
                StaffInCamp.id.label("staff_in_camp_id"),
                Camp.id.label("camp_id"),
                Camp.name.label("camp_name"),
                Location.name.label("location_name"),
                Camp.public_price.label("public_price"),
                Camp.start.label("camp_start"),
                Camp.end.label("camp_end"),
            )
            .join(StaffInCamp, StaffInCamp.camp_id == Camp.id)
            .join(Location, Camp.location_id == Location.id)
            .filter(
                and_(
                    StaffInCamp.staff_id == staff_id,
                    StaffInCamp.confirmed_staff == True,
                    Camp.active == True,
                    Camp.end >= date.today(),
                )
            )
            .all()
        )

        staff_camps = db_mapping_rows_to_dict(staff_camps)
        staff_camps_final = []

        for staff_in_camp in staff_camps:
            camps_id.append(staff_in_camp["camp_id"])
            records = get_records_for_camp(db, staff_in_camp["camp_id"])
            staff_in_camp = dict(staff_in_camp)
            staff_in_camp["records"] = records
            staff_camps_final.append(staff_in_camp)

        next_camps = (
            db.query(
                Camp.id.label("camp_id"),
                Camp.name.label("camp_name"),
                Location.name.label("location_name"),
                Camp.public_price.label("public_price"),
                Camp.start.label("camp_start"),
                Camp.end.label("camp_end"),
            )
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
        next_camps_filter = [d for d in next_camps if d["camp_id"] not in camps_id]
        next_camps_final = []

        for camp in next_camps_filter:
            records = get_records_for_camp(db, camp["camp_id"])
            camp = dict(camp)
            camp["records"] = records
            next_camps_final.append(camp)

        return {
            "available_camps": available_camps_final,
            "staff_camps": staff_camps_final,
            "next_camps": next_camps_final,
        }

    else:
        complete_profile = True if user[2] else False
        return {
            "is_active": user[0],
            "is_employee": user[1],
            "complete_profile": complete_profile,
        }


def get_staff_by_id(db, staff_id: int):
    staff = db.query(Staff).filter_by(id=staff_id).first()
    return staff


def get_staff_band(db, staff_id: int):
    staff_band = (
        db.query(
            (
                Staff.name + " " + Staff.lastname_father + " " + Staff.lastname_mother
            ).label("staff_full_name"),
            Staff.birthday.label("staff_birthday"),
            Staff.photo.label("staff_photo"),
            StaffRecord.attended.label("camp_attended"),
            StaffRecord.attend.label("camp_attend"),
        )
        .outerjoin(StaffRecord, StaffRecord.id == Staff.record_id)
        .filter(Staff.id == staff_id)
        .all()
    )
    return db_mapping_rows_to_dict(staff_band)

def get_staff_vaccines(db: Session, staff_id):
    query = ( db.query(
                Vaccine.id,
                Vaccine.name,
                StaffVaccine.is_active)
             .select_from(StaffVaccine)
             .join(Vaccine, StaffVaccine.vaccine_id == Vaccine.id)
             .join(Staff, Staff.id == StaffVaccine.staff_id)
             .filter(Staff.id == staff_id)
             
            )
    data = db.execute(query)
    data = data.mappings().all()
    return data
def get_staff_food_restriction(db: Session, staff_id):
    query = ( db.query(
                FoodRestriction.id,
                FoodRestriction.name,
                StaffFoodRestriction.is_active)
             .select_from(StaffFoodRestriction)
             .join(Staff, Staff.id == StaffFoodRestriction.staff_id)
             .join(FoodRestriction, FoodRestriction.id == StaffFoodRestriction.food_restriction_id)
             .filter(Staff.id == staff_id)
            
            )
    data = db.execute(query)
    data = data.mappings().all()
    return data