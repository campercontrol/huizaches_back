from sqlalchemy import and_, func, extract
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from utils.db import db_mapping_rows_to_dict
from datetime import date
from model.camps import Camp, Location, CampPaymentAccount, CamperInCamp
from model.campers import Camper
from model.campers.parent import Parent
from model.user import User
from model.payments.payment import Payment
from model.payments.payment_method import PaymentMethod
from model.catalogs import (
    Constant
)
from model.campers import (
    School    
)
from schema.camps.camp_schema import CampCreate, CampModify
from crud.campers.camper_crud import get_pathological_background_by_camper, get_camper_licensed_medicine, get_extra_charge_by_camper_camp, get_camper_vaccines
from crud.camps.camper_in_camp_crud import get_campers_for_module
from crud.camps.staff_in_camp_crud import get_staff_volunteer_in_camp, get_staff_in_camp
from crud.campers_catalogs.camper_food_restriction_crud import get_camper_food_restriction
from crud.campers.camper_comment_crud import get_camper_comment_by_camper_for_admin, get_camper_comment_by_camper_for_parent, get_camper_comment_by_camper_for_school



def get_camp_insr_report(db: Session, camp_id: int):
    catalog_gender = aliased(Constant)
    query = (db.query(Camper.id,
                      Camper.name,
                      Camper.lastname_father,
                      Camper.lastname_mother,
                      Camper.birthday,
                      func.concat(extract('year', func.age(func.current_date(), Camper.birthday)), " years ",  extract('month', func.age(func.current_date(), Camper.birthday)), " months ").label("Age"),
                      catalog_gender.value.label('gender'),
                      ).select_from(CamperInCamp)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(catalog_gender, Camper.gender_id == catalog_gender.id)
             .filter(CamperInCamp.camp_id == camp_id))
    campers = db.execute(query)
    campers = campers.mappings().all()
    
    return campers


def get_camp_incomes(db: Session, camp_id: int):
    
    payment_methods = db.query(PaymentMethod).all()
    incomes_per_payment_method = []
    for payment_method in payment_methods:
        total_payment_amount = db.query(func.sum(func.abs(Payment.payment_amount))).select_from(Payment).filter(and_(Payment.camp_id == camp_id, Payment.payment_method_id == payment_method.id)).scalar()
        total_transactions_per_payment_method = db.query(func.count(Payment.id)).select_from(Payment).filter(and_(Payment.camp_id == camp_id, Payment.payment_method_id == payment_method.id)).scalar()
        income = {
            "payment_method": payment_method.name,
            "transactions": total_transactions_per_payment_method,
            "total_amount": total_payment_amount or 0
        }
        incomes_per_payment_method.append(income)
    
    total_discount_amount = db.query(func.sum(func.abs(Payment.payment_amount))).select_from(Payment).filter(and_(Payment.camp_id == camp_id, Payment.txn_type_id == 2)).scalar()   
    total_transactions_per_discount = db.query(func.count(Payment.id)).select_from(Payment).filter(and_(Payment.camp_id == camp_id, Payment.txn_type_id == 2)).scalar()

    discount_income = {
        "payment_method": "Descuentos",
        "transactions": total_transactions_per_discount,
        "total_amount": total_discount_amount or 0
    }
    incomes_per_payment_method.append(discount_income)
    
    return incomes_per_payment_method
    
        
def get_camp_contact_report(db: Session, camp_id: int):
    
    query = (db.query(Camper.id,
                      Camper.name,
                      Camper.lastname_father,
                      Camper.lastname_mother,
                      Parent.tutor_name,
                      Parent.tutor_lastname_father,
                      Parent.tutor_lastname_mother,
                      Parent.tutor_cellphone,
                      Parent.tutor_home_phone,
                      Parent.tutor_work_phone,
                      User.email.label("tutor_email"),
                      Parent.contact_name.label("second_tutor_name"),
                      Parent.contact_lastname_father.label("second_tutor_mothers_lastname"),
                      Parent.contact_lastname_mother.label("second_tutor_fathers_lastname"),
                      Parent.contact_cellphone.label("second_tutor_cellphone"),
                      Parent.contact_home_phone.label("second_tutor_fathers_lastname"),
                      Parent.contact_work_phone.label("second_tutor_work_phone"),
                      Parent.contact_email.label("second_tutor_email"),
                      Camper.contact_name.label("emergency_contact"),
                      Camper.contact_relation.label("emergency_contact_kinship"),
                      Camper.contact_homephone.label("emergency_contact_phone"),
                      Camper.contact_cellphone.label("emergency_contact_cellphone")                      
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(Parent, Camper.parent_id == Parent.id)
             .join(User, Parent.user_id == User.id)
             .filter(CamperInCamp.camp_id == camp_id))
    campers = db.execute(query)
    campers = campers.mappings().all()
    return campers

def get_camp_contact_report(db: Session, camp_id: int):
    
    query = (db.query(Camper.id,
                      Camper.name,
                      Camper.lastname_father,
                      Camper.lastname_mother,
                      Parent.tutor_name,
                      Parent.tutor_lastname_father,
                      Parent.tutor_lastname_mother,
                      Parent.tutor_cellphone,
                      Parent.tutor_home_phone,
                      Parent.tutor_work_phone,
                      User.email.label("tutor_email"),
                      Parent.contact_name.label("second_tutor_name"),
                      Parent.contact_lastname_father.label("second_tutor_mothers_lastname"),
                      Parent.contact_lastname_mother.label("second_tutor_fathers_lastname"),
                      Parent.contact_cellphone.label("second_tutor_cellphone"),
                      Parent.contact_home_phone.label("second_tutor_fathers_lastname"),
                      Parent.contact_work_phone.label("second_tutor_work_phone"),
                      Parent.contact_email.label("second_tutor_email"),
                      Camper.contact_name.label("emergency_contact"),
                      Camper.contact_relation.label("emergency_contact_kinship"),
                      Camper.contact_homephone.label("emergency_contact_phone"),
                      Camper.contact_cellphone.label("emergency_contact_cellphone")                      
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(Parent, Camper.parent_id == Parent.id)
             .join(User, Parent.user_id == User.id)
             .filter(CamperInCamp.camp_id == camp_id))
    campers = db.execute(query)
    campers = campers.mappings().all()
    return campers


def get_camp_medical_report(db: Session, camp_id: int):

    catalog_gender = aliased(Constant)
    catalog_swim =  aliased(Constant)
    catalog_blood_type =  aliased(Constant)

    query = (db.query(Camper.id,
                      Camper.name,
                      Camper.lastname_father,
                      Camper.lastname_mother,
                      func.concat(extract('year', func.age(func.current_date(), Camper.birthday)), " years ",  extract('month', func.age(func.current_date(), Camper.birthday)), " months ").label("Age"),
                      Camper.height,
                      Camper.weight,
                      catalog_gender.value.label('gender'),
                      catalog_swim.value.label('swim'),
                      Camper.affliction,
                      catalog_blood_type.value.label('blood_type'),
                      Camper.heart_problems,
                      Camper.psicology_treatments,
                      Camper.prevent_activities,
                      Camper.other_allergies,
                      Camper.nocturnal_disorders,
                      Camper.phobias,
                      Camper.drugs,
                      Camper.doctor_precall,
                      Camper.prohibited_foods,
                      Camper.insurance,
                      Camper.insurance_number,
                      Camper.security_social_number,
                      Parent.tutor_name,
                      Parent.tutor_lastname_father,
                      Parent.tutor_lastname_mother,
                      Parent.tutor_cellphone,
                      Parent.tutor_home_phone,
                      Parent.tutor_work_phone,
                      User.email.label("tutor_email"),
                      Parent.contact_name.label("second_tutor_name"),
                      Parent.contact_lastname_father.label("second_tutor_mothers_lastname"),
                      Parent.contact_lastname_mother.label("second_tutor_fathers_lastname"),
                      Parent.contact_cellphone.label("second_tutor_cellphone"),
                      Parent.contact_home_phone.label("second_tutor_fathers_lastname"),
                      Parent.contact_work_phone.label("second_tutor_work_phone"),
                      Parent.contact_email.label("second_tutor_email"),
                      Camper.contact_name.label("emergency_contact"),
                      Camper.contact_relation.label("emergency_contact_kinship"),
                      Camper.contact_cellphone.label("emergency_contact_cellphone"),
                      Camper.contact_homephone.label("emergency_home_phone")                      
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(catalog_gender, Camper.gender_id == catalog_gender.id)
             .join(catalog_swim, Camper.can_swim == catalog_swim.id)
             .join(catalog_blood_type, Camper.blood_type == catalog_blood_type.id)
             .join(Parent, Camper.parent_id == Parent.id)
             .join(User, Parent.user_id == User.id)
             .filter(CamperInCamp.camp_id == camp_id))
    campers = db.execute(query)
    campers = campers.mappings().all()
    
    campers_report = []
   
    for camper in campers:
        camper_dict = dict(camper)
        camper_pathological_background = get_pathological_background_by_camper(db, camper.id) 
        camper_food_restriction = get_camper_food_restriction(db, camper.id)
        camper_licensed_medicine = get_camper_licensed_medicine(db, camper.id)
        camper_vaccines = get_camper_vaccines(db, camper.id)
        
        for pathological_background in camper_pathological_background:
            camper_dict[pathological_background["name"]] = pathological_background["is_active"]
        
        for food_restriction in camper_food_restriction:
            camper_dict[food_restriction["name"]] = food_restriction["is_active"]
        
        for vaccines in camper_vaccines:
            camper_dict[vaccines["name"]] = vaccines["is_active"]
            
        for licensed_medicine in camper_licensed_medicine:
            camper_dict[licensed_medicine["name"]] = licensed_medicine["is_active"]
            
        campers_report.append(camper_dict)
    
    return campers_report
    


def get_camp_gnl_report(db: Session, camp_id: int):

    catalog_gender = aliased(Constant)
    catalog_grade = aliased(Constant)
    catalog_swim =  aliased(Constant)
    catalog_blood_type =  aliased(Constant)



    query = (db.query(Camper.id,
                      Camper.name,
                      Camper.lastname_father,
                      Camper.lastname_mother,
                      Camper.birthday,
                      Camper.height,
                      Camper.weight,
                      catalog_gender.value.label('gender'),
                      catalog_grade.value.label('grade'),
                      School.name.label("school"),
                      Camper.school_other,
                      catalog_swim.value.label('swim'),
                      Camper.affliction,
                      catalog_blood_type.value.label('blood_type'),
                      Camper.heart_problems,
                      Camper.psicology_treatments,
                      Camper.prevent_activities,
                      Camper.other_allergies,
                      Camper.nocturnal_disorders,
                      Camper.phobias,
                      Camper.drugs,
                      Camper.doctor_precall,
                      Camper.prohibited_foods,
                      Camper.comments_admin,
                      Camper.insurance_company,
                      Camper.insurance_number,
                      Camper.security_social_number,
                      Parent.tutor_name,
                      Parent.tutor_lastname_father,
                      Parent.tutor_lastname_mother,
                      Parent.tutor_cellphone,
                      Parent.tutor_home_phone,
                      Parent.tutor_work_phone,
                      User.email.label("tutor_email"),
                      Parent.contact_name.label("second_tutor_name"),
                      Parent.contact_lastname_father.label("second_tutor_mothers_lastname"),
                      Parent.contact_lastname_mother.label("second_tutor_fathers_lastname"),
                      Parent.contact_cellphone.label("second_tutor_cellphone"),
                      Parent.contact_home_phone.label("second_tutor_fathers_lastname"),
                      Parent.contact_work_phone.label("second_tutor_work_phone"),
                      Parent.contact_email.label("second_tutor_email"),
                      Camper.contact_name.label("emergency contact"),
                      Camper.contact_relation.label("contact kinship"),
                      Camper.contact_cellphone,
                      Camper.contact_homephone,
                      CamperInCamp.payment_balance,
                      Camper.created_at.label("registration date")
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(catalog_gender, Camper.gender_id == catalog_gender.id)
             .join(catalog_grade, Camper.grade == catalog_grade.id)
             .join(catalog_swim, Camper.can_swim == catalog_swim.id)
             .join(catalog_blood_type, Camper.blood_type == catalog_blood_type.id)
             .join(Parent, Camper.parent_id == Parent.id)
             .join(User, Parent.user_id == User.id)
             .join(School, Camper.school_id== School.id)
             .filter(CamperInCamp.camp_id == camp_id))
    campers = db.execute(query)
    campers = campers.mappings().all()

    campers_report = []
   
    for camper in campers:
        camper_dict = dict(camper)
        camper_pathological_background = get_pathological_background_by_camper(db, camper.id) 
        camper_food_restriction = get_camper_food_restriction(db, camper.id)
        camper_licensed_medicine = get_camper_licensed_medicine(db, camper.id)
        camper_vaccines = get_camper_vaccines(db, camper.id)
        camper_extra_charges = get_extra_charge_by_camper_camp(db, camper.id, camp_id)
        camper_parent_comments = get_camper_comment_by_camper_for_parent(db, camper.id)
        camper_school_comments = get_camper_comment_by_camper_for_school(db, camper.id)
        camper_admin_comments = get_camper_comment_by_camper_for_admin(db, camper.id)
        
        for pathological_background in camper_pathological_background:
            camper_dict[pathological_background["name"]] = pathological_background["is_active"]
        
        for food_restriction in camper_food_restriction:
            camper_dict[food_restriction["name"]] = food_restriction["is_active"]
        
        for vaccines in camper_vaccines:
            camper_dict[vaccines["name"]] = vaccines["is_active"]
            
        for licensed_medicine in camper_licensed_medicine:
            camper_dict[licensed_medicine["name"]] = licensed_medicine["is_active"]
            
        for extra_charge in camper_extra_charges:
            extracharge_column_name = f"{extra_charge['name']} ${extra_charge['price']}"
            camper_dict[extracharge_column_name] = extra_charge["is_selected"]
        
        camper_dict["Comments (Parent)"] = camper_parent_comments
        camper_dict["Comments (Staff)"] = camper_admin_comments
        camper_dict["Comments (School)"] = camper_school_comments
        campers_report.append(camper_dict)
        
    return campers_report

def get_camp_food_report(db: Session, camp_id: int):

    query = (db.query(Camper.id,
                      Camper.name,
                      Camper.lastname_father,
                      Camper.lastname_mother,
                      Camper.other_allergies,
                      Camper.prohibited_foods
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .filter(CamperInCamp.camp_id == camp_id))
    campers = db.execute(query)
    campers = campers.mappings().all()

    campers_report = []
   
    for camper in campers:
        camper_dict = dict(camper)
        camper_food_restriction = get_camper_food_restriction(db, camper.id)
        
        for food_restriction in camper_food_restriction:
            camper_dict[food_restriction["name"]] = food_restriction["is_active"]
        
        campers_report.append(camper_dict)
        
    return campers_report

def get_camp_social_report(db: Session, camp_id: int):

    catalog_gender = aliased(Constant)
    catalog_grade = aliased(Constant)
    catalog_swim =  aliased(Constant)

    query = (db.query(Camper.id,
                      Camper.name,
                      Camper.lastname_father,
                      Camper.lastname_mother,
                      Camper.birthday,
                      catalog_gender.value.label('gender'),
                      catalog_grade.value.label('grade'),
                      Camper.prevent_activities,
                      Camper.psicology_treatments,
                      Camper.nocturnal_disorders,
                      Camper.phobias,
                      Camper.drugs,
                      catalog_swim.value.label('swim')
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(catalog_gender, Camper.gender_id == catalog_gender.id)
             .join(catalog_grade, Camper.grade == catalog_grade.id)
             .join(catalog_swim, Camper.can_swim == catalog_swim.id)
             .filter(CamperInCamp.camp_id == camp_id))
    campers = db.execute(query)
    campers = campers.mappings().all()

    campers_report = []
   
    for camper in campers:
        camper_dict = dict(camper)
        camper_parent_comments = get_camper_comment_by_camper_for_parent(db, camper.id)
        camper_school_comments = get_camper_comment_by_camper_for_school(db, camper.id)
        camper_admin_comments = get_camper_comment_by_camper_for_admin(db, camper.id)
                
        camper_dict["Comments (Parent)"] = camper_parent_comments
        camper_dict["Comments (Staff)"] = camper_admin_comments
        camper_dict["Comments (School)"] = camper_school_comments
        campers_report.append(camper_dict)
        
    return campers_report

def get_camp_extras_report(db: Session, camp_id: int):

    query = (db.query(Camper.id,
                      Camper.name,
                      Camper.lastname_father,
                      Camper.lastname_mother,
                      CamperInCamp.payment_balance
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .filter(CamperInCamp.camp_id == camp_id))
    campers = db.execute(query)
    campers = campers.mappings().all()

    campers_report = []
   
    for camper in campers:
        camper_dict = dict(camper)

        camper_extra_charges = get_extra_charge_by_camper_camp(db, camper.id, camp_id)
         
        for extra_charge in camper_extra_charges:
            extracharge_column_name = f"{extra_charge['name']} ${extra_charge['price']}"
            camper_dict[extracharge_column_name] = extra_charge["is_selected"]

        campers_report.append(camper_dict)
        
    return campers_report

def get_all_camp(db: Session):
    rows = db.query(Camp).all()
    return rows


def get_all_active_camp(db: Session):
    camps = []
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.public_price.label("camp_public_price"),
            Camp.show_payment_parent.label("camp_show_payment_parent"),
            Location.name.label("location_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end")
        )
        .join(Location, Location.id == Camp.location_id)
        .filter(Camp.active==True)
        .all()
    )
    for row in db_mapping_rows_to_dict(rows):
        records = get_records_for_camp(db, row.camp_id)
        row = dict(row)
        row["records"] = records
        camps.append(row)

    return camps


def get_school_camp_for_camper(db: Session, camper_id: int):
    school_id = db.query(Camper.school_id).filter_by(id=camper_id).first()
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
        )
        .join(Location, Location.id == Camp.location_id)
        .filter(
            and_(
                Camp.general_camp == False,
                Camp.school_id == school_id[0],
                Camp.active == True,
                Camp.start >= date.today(),
                Camp.registration == True,
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_summer_camp_for_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
        )
        .join(Location, Location.id == Camp.location_id)
        .filter(
            and_(
                Camp.general_camp == True,
                Camp.active == True,
                Camp.start >= date.today(),
                Camp.registration == True,
            )
        )
    )
    return db_mapping_rows_to_dict(rows)


def get_camp_by_id(db: Session, camp_id: int):
    return db.query(Camp).filter_by(id=camp_id).first()

def get_camp_info_by_id_mailing(db: Session, camp_id: int):
    query = db.query(Camp.id,
                     Camp.name,
                     Camp.start,
                     Camp.end,
                     Camp.start_registration,
                     Camp.end_registration,
                     Camp.registration,
                     Camp.url,
                     Camp.special_message,
                     Camp.special_message,
                     Camp.special_message_admin,
                     Camp.public_price,
                     Camp.insurance,
                     Camp.venue,
                     Camp.photo_url,
                     Camp.photo_password,
                     Camp.medical_report,
                     Camp.occupancy_camp,
                     School.name.label("school"),
                     Location.name.label("location")
                     ).join(School, School.id == Camp.school_id).join(Location, Location.id == Camp.location_id).filter(Camp.id == camp_id)
    data = db.execute(query)
    return data.mappings().first()
def create_new_camp(db: Session, new_camp: CampCreate):
    db_camp = None
    try:
        db_camp = Camp(**new_camp.dict())
        db.add(db_camp)
        db.commit()
        db.refresh(db_camp)
    except SQLAlchemyError as e:
        print("#========================#")
        print(e)
        print("#========================#")
        db_camp = None
        return db_camp
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camp


def update_camp_by_id(db: Session, camp_id: int, modify_camp: CampModify):
    rows_updated = (
        db.query(Camp)
        .filter_by(id=camp_id)
        .update(modify_camp, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def delete_camp(db: Session, camp_id: int):
    camp = db.query(Camp).filter(Camp.id == camp_id).first()
    db.delete(camp)
    db.commit()
    return {"status": True}


def get_records_for_camp(db: Session, camp_id: int):
    campers_record = len(get_campers_for_module(db, camp_id))
    staff_available_record = len(get_staff_volunteer_in_camp(db, camp_id))
    staff_record = len(get_staff_in_camp(db, camp_id))

    return {
        "campers_recod": campers_record,
        "staff_available_record": staff_available_record,
        "staff_record": staff_record,
    }


# 2


def get_camp_by_search(db: Session, search: str):
    camps = (
        db.query(Camp.id.label("camp_id"), Camp.name.label("camp_name"))
        .filter(Camp.name.ilike(r"%{}%".format(search)))
        .all()
    )

    if not camps:
        return "Data not found"

    return db_mapping_rows_to_dict(camps)


def get_camp_by_search(db: Session, search: str):
    camps = (
        db.query(Camp.id.label("camp_id"), Camp.name.label("camp_name"))
        .filter(Camp.name.ilike(r"%{}%".format(search)))
        .all()
    )

    if not camps:
        return "Data not found"

    return db_mapping_rows_to_dict(camps)

def get_school_info_by_camp(db: Session, camp_id:int):
    query = (db.query(School.id.label('school_id'), School.name, School.email, School.contact_second_email, School.contact_third_email ).join(Camp, Camp.school_id == School.id))
    data = db.execute(query)
    return data.mappings().first()

def create_new_camp_payment_account(db: Session, new_camp_payment_account):
    db_camp_payment_account = None
    try:
        db_camp_payment_account = CampPaymentAccount(**new_camp_payment_account.dict())
        db.add(db_camp_payment_account)
        db.commit()
        db.refresh(db_camp_payment_account)
    except SQLAlchemyError as e:
        db.rollback()
        print("#========================#")
        print(e)
        print("#========================#")
        db_camp_payment_account = None
        return db_camp_payment_account
    except Exception as ex:
        db.rollback()
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camp_payment_account
