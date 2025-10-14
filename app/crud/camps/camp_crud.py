from sqlalchemy import and_, func, extract, select, desc,asc, or_, text
import os
from math import ceil
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from utils.db import db_mapping_rows_to_dict
from utils.formatters import format_numbers_commas_currency
from datetime import date
from model.camps import Camp, Location, CampPaymentAccount, CamperInCamp
from model.campers.camper_comment import CamperComment
from model.campers import Camper
from model.campers.parent import Parent
from model.user import User
from model.payments.payment import Payment
from model.payments.payment_method import PaymentMethod
from model.camps.staff_in_camp import StaffInCamp
from model.staffs.staff import Staff
from model.medical.medical_camper_visit import MedicalCamperVisit
from model.catalogs import (
    Constant
)
from model.campers import (
    School    
)
from model.catalogs.currency import Currency
from schema.camps.camp_schema import CampCreate, CampModify
from schema.pagination.pagination_schema import Pagination, SortEnum
from crud.campers.camper_crud import get_pathological_background_by_camper, get_camper_licensed_medicine, get_extra_charge_by_camper_camp, get_camper_vaccines
from crud.camps.camper_in_camp_crud import get_campers_for_module_count
from crud.camps.staff_in_camp_crud import get_staff_volunteer_in_camp_count, get_staff_in_camp_count
from crud.campers_catalogs.camper_food_restriction_crud import get_camper_food_restriction
from crud.campers.camper_comment_crud import get_camper_comment_by_camper_for_admin, get_camper_comment_by_camper_for_parent, get_camper_comment_by_camper_for_school
from crud.staff_catalogs.staff_food_restriction_crud import get_all_staff_food_restriction_by_id
from crud.staff_catalogs.staff_vaccine_crud import get_staff_all_vaccines_by_staff_id
from crud.groupings.grouping_camp_crud import get_camper_groupings_by_camper_id_and_camp_id

from helper.pagination_helpers import pagination_params, get_number_of_pages

BACKEND_DEV_URL = os.getenv("BACKEND_PROD_URL")

def get_camp_insr_report(db: Session, camp_id: int):
    catalog_gender = aliased(Constant)
    catalog_camp_enrollment = aliased(Constant)
    query = (db.query(Camper.id,
                      Camper.name,
                      Camper.lastname_father,
                      Camper.lastname_mother,
                      Camper.birthday,
                      func.concat(extract('year', func.age(func.current_date(), Camper.birthday)), " years ",  extract('month', func.age(func.current_date(), Camper.birthday)), " months ").label("Age"),
                      catalog_gender.value.label('gender'),
                      catalog_camp_enrollment.value.label("enrollment")
                      ).select_from(CamperInCamp)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(catalog_camp_enrollment, CamperInCamp.status == catalog_camp_enrollment.id)
             .join(catalog_gender, Camper.gender_id == catalog_gender.id)
             .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36)))
    campers = db.execute(query)
    campers = campers.mappings().all()
    
    return campers


def get_camp_incomes(db: Session, camp_id: int):
    camp_and_camper_payments_info = {}
    payment_methods = db.query(PaymentMethod).all()
    camp_info = (
        db.query(Camp.id, Currency.symbol, Currency.acronyms)
        .select_from(Camp)
        .join(Currency, Currency.id == Camp.currency_id)
        .filter(Camp.id == camp_id).first()
    )
    incomes_per_payment_method = []
    for payment_method in payment_methods:
        total_payment_amount = (
            db.query(func.sum(func.abs(Payment.payment_amount)))
            .select_from(Payment)
            .filter(Payment.camp_id == camp_id, Payment.payment_method_id == payment_method.id, or_(Payment.txn_type_id == 3, Payment.txn_type_id == 6, Payment.txn_type_id ==7)).scalar()
        
        )
        total_transactions_per_payment_method = (
            db.query(func.count(Payment.id))
            .select_from(Payment)
            .filter(Payment.camp_id == camp_id, Payment.payment_method_id == payment_method.id, or_(Payment.txn_type_id == 3, Payment.txn_type_id == 6, Payment.txn_type_id ==7)).scalar()
            
        )

        
        income = {
            "payment_method": payment_method.name,
            "transactions": total_transactions_per_payment_method,
            "total_amount": format_numbers_commas_currency(total_payment_amount or 0, camp_info.symbol, camp_info.acronyms)
        }
        incomes_per_payment_method.append(income)
    
    total_discount_amount = db.query(func.sum(func.abs(Payment.payment_amount))).select_from(Payment).filter(and_(Payment.camp_id == camp_id, Payment.txn_type_id == 2)).scalar()   
    total_transactions_per_discount = db.query(func.count(Payment.id)).select_from(Payment).filter(and_(Payment.camp_id == camp_id, Payment.txn_type_id == 2)).scalar()

    discount_income = {
        "payment_method": "Descuentos",
        "transactions": total_transactions_per_discount,
        "total_amount": format_numbers_commas_currency(total_discount_amount or 0, camp_info.symbol, camp_info.acronyms)
    }
    incomes_per_payment_method.append(discount_income)
    
    campers_in_camp = db.query(CamperInCamp.id, CamperInCamp.payment_balance, CamperInCamp.camp_id, CamperInCamp.camper_id, Constant.value).select_from(CamperInCamp).join(Constant, Constant.id == CamperInCamp.status).filter(CamperInCamp.camp_id == camp_id).all()
    if campers_in_camp:

        campers_and_payments_info = []
        for camper in campers_in_camp:
            camper_payments_by_method = []
            camper_payments_info = {}
            payment_info = {}
            camper_info = db.query(Camper).select_from(Camper).filter(Camper.id == camper.camper_id).first()
            for payment_method in payment_methods:
                camper_payments_by_payment_method_total_amount = db.query(func.sum(func.abs(Payment.payment_amount))).select_from(Payment).filter(and_(Payment.camper_id == camper.camper_id, Payment.camp_id == camp_id, Payment.payment_method_id == payment_method.id)).scalar()
                camper_total_transactions_by_payment_method = db.query(func.count(Payment.id)).select_from(Payment).filter(and_(Payment.camper_id == camper.camper_id, Payment.camp_id == camp_id, Payment.payment_method_id == payment_method.id)).scalar()
                camper_payment_by_method_id = {
                    "id": payment_method.id,
                    "payment_method": payment_method.name,
                    "total_amount": format_numbers_commas_currency(camper_payments_by_payment_method_total_amount or 0, camp_info.symbol, camp_info.acronyms),
                    "transactions": camper_total_transactions_by_payment_method or 0
                }
                camper_payments_by_method.append(camper_payment_by_method_id)
            # camper comments
            total_camper_comments = db.query(func.count(CamperComment.id)).select_from(CamperComment).filter(CamperComment.camper_id == camper.camper_id).scalar() 
            # total_amount, and count of all payments
            camper_payments_total_amount = db.query(func.sum(func.abs(Payment.payment_amount))).select_from(Payment).filter(and_(Payment.camper_id == camper.camper_id, Payment.camp_id == camp_id, Payment.txn_type_id == 3)).scalar()
            camper_payments_total_transactions = db.query(func.count(Payment.id)).select_from(Payment).filter(and_(Payment.camper_id == camper.camper_id, Payment.camp_id == camp_id, Payment.txn_type_id == 3)).scalar()

            total_payments = {
                "amount": format_numbers_commas_currency(camper_payments_total_amount or 0, camp_info.symbol, camp_info.acronyms),
                "number_of_payments": camper_payments_total_transactions or 0
            }
            #total amount of discounts by camper
            camper_total_discount_amount = db.query(func.sum(func.abs(Payment.payment_amount))).select_from(Payment).filter(and_(Payment.camp_id == camp_id, Payment.camper_id == camper.camper_id, Payment.txn_type_id == 2)).scalar()   
            camper_total_transactions_per_discount = db.query(func.count(Payment.id)).select_from(Payment).filter(and_(Payment.camp_id == camp_id, Payment.camper_id == camper.camper_id, Payment.txn_type_id == 2)).scalar()

            discounts = {
                "amount": format_numbers_commas_currency(camper_total_discount_amount or 0, camp_info.symbol, camp_info.acronyms), 
                "number_of_discounts": camper_total_transactions_per_discount or 0
            }
            
            #total amount of refunds
            camper_total_refund_amount = db.query(func.sum(func.abs(Payment.payment_amount))).select_from(Payment).filter(and_(Payment.camp_id == camp_id, Payment.camper_id == camper.camper_id, Payment.txn_type_id == 4)).scalar() 
            camper_total_refund_transactions = db.query(func.count(Payment.id)).select_from(Payment).filter(and_(Payment.camp_id == camp_id, Payment.camper_id == camper.camper_id, Payment.txn_type_id == 4)).scalar()

            refunds = {
                "amount": format_numbers_commas_currency(camper_total_refund_amount or 0, camp_info.symbol, camp_info.acronyms),
                "number_of_refunds": camper_total_refund_transactions or 0
            }
            camp_status = {
                "balance": format_numbers_commas_currency(camper.payment_balance or 0, camp_info.symbol, camp_info.acronyms),
                "enrolment_status": camper.value
            }
            
            payment_info["payments_by_payment_method"] = camper_payments_by_method
            payment_info["total_payments"] = total_payments
            payment_info["discounts"] = discounts
            payment_info["refunds"] = refunds
            payment_info["camp_status"] = camp_status
            
            camper_payments_info["camper_id"] = camper_info.id
            camper_payments_info["camper_fullname"] = camper_info.name + " " + camper_info.lastname_father + " " + camper_info.lastname_mother
            camper_payments_info["number_of_comments"] = total_camper_comments
            camper_payments_info["payments_info"] = payment_info

            campers_and_payments_info.append(camper_payments_info)
            
            camp_and_camper_payments_info["camp_incomes_per_payment_method"] = incomes_per_payment_method
            camp_and_camper_payments_info["camper_payments"] = campers_and_payments_info
    else:
        camp_and_camper_payments_info["camp_incomes_per_payment_method"] = incomes_per_payment_method
        camp_and_camper_payments_info["camper_payments"] = []
    
    
    return camp_and_camper_payments_info
    
        
def get_camp_contact_report(db: Session, camp_id: int):
    
    catalog_camp_enrollment = aliased(Constant)
    
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
                      Camper.contact_cellphone.label("emergency_contact_cellphone"),
                      catalog_camp_enrollment.value.label("enrollment")                      
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(catalog_camp_enrollment, CamperInCamp.status == catalog_camp_enrollment.id)
             .join(Parent, Camper.parent_id == Parent.id)
             .join(User, Parent.user_id == User.id)
             .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36)))
    campers = db.execute(query)
    campers = campers.mappings().all()
    return campers


def get_camp_medical_report(db: Session, camp_id: int):

    catalog_gender = aliased(Constant)
    catalog_swim =  aliased(Constant)
    catalog_blood_type =  aliased(Constant)
    catalog_camp_enrollment = aliased(Constant)

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
                      Camper.contact_homephone.label("emergency_home_phone"),
                      catalog_camp_enrollment.value.label("enrollment")                      
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(catalog_gender, Camper.gender_id == catalog_gender.id)
             .join(catalog_swim, Camper.can_swim == catalog_swim.id)
             .join(catalog_blood_type, Camper.blood_type == catalog_blood_type.id)
             .join(catalog_camp_enrollment, CamperInCamp.status == catalog_camp_enrollment.id)
             .join(Parent, Camper.parent_id == Parent.id)
             .join(User, Parent.user_id == User.id)
             .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36)))
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
    catalog_camp_enrollment = aliased(Constant)



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
                      Camper.created_at.label("registration date"),
                      catalog_camp_enrollment.value.label("enrollment")
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(catalog_gender, Camper.gender_id == catalog_gender.id)
             .join(catalog_grade, Camper.grade == catalog_grade.id)
             .join(catalog_swim, Camper.can_swim == catalog_swim.id)
             .join(catalog_blood_type, Camper.blood_type == catalog_blood_type.id)
             .join(catalog_camp_enrollment, CamperInCamp.status == catalog_camp_enrollment.id)
             .join(Parent, Camper.parent_id == Parent.id)
             .join(User, Parent.user_id == User.id)
             .join(School, Camper.school_id== School.id)
             .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36)))
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
        camper_groupings = get_camper_groupings_by_camper_id_and_camp_id(db, camper.id, camp_id)
        
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
        camper_dict["Groupings"] = camper_groupings
        campers_report.append(camper_dict)
        
    return campers_report

def get_camp_food_report(db: Session, camp_id: int):

    catalog_camp_enrollment = aliased(Constant)
    query = (db.query(Camper.id,
                      Camper.name,
                      Camper.lastname_father,
                      Camper.lastname_mother,
                      Camper.other_allergies,
                      Camper.prohibited_foods,
                      catalog_camp_enrollment.value.label("enrollment")
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(catalog_camp_enrollment, CamperInCamp.status == catalog_camp_enrollment.id)
             .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36)))
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
    catalog_camp_enrollment = aliased(Constant)

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
                      catalog_swim.value.label('swim'),
                      catalog_camp_enrollment.value.label("enrollment")
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(catalog_gender, Camper.gender_id == catalog_gender.id)
             .join(catalog_grade, Camper.grade == catalog_grade.id)
             .join(catalog_swim, Camper.can_swim == catalog_swim.id)
             .join(catalog_camp_enrollment, CamperInCamp.status == catalog_camp_enrollment.id)
             .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36)))
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
    
    catalog_camp_enrollment = aliased(Constant)
    query = (db.query(Camper.id,
                      Camper.name,
                      Camper.lastname_father,
                      Camper.lastname_mother,
                      CamperInCamp.payment_balance,
                      catalog_camp_enrollment.value.label("enrollment")
                      ).select_from(CamperInCamp)
             .join(Camp, CamperInCamp.camp_id == Camp.id)
             .join(Camper, CamperInCamp.camper_id == Camper.id)
             .join(catalog_camp_enrollment, CamperInCamp.status == catalog_camp_enrollment.id)
             .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36)))
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


def get_camp_medical_visit_report(db: Session, camp_id: int):
    query = (db.query(
                        func.concat(Camper.name, ' ', Camper.lastname_father, ' ', Camper.lastname_mother).label('Nombre del camper'),
                        MedicalCamperVisit.id,
                        MedicalCamperVisit.attention_date.label('Fecha de consulta'),
                        MedicalCamperVisit.attention_time.label('Hora de consulta'),
                        MedicalCamperVisit.diagnostic.label('Diagnostico'),
                        MedicalCamperVisit.doctor.label('Doctor que atendió'),
                        MedicalCamperVisit.description.label('Descripción de la lesión'),
                        Constant.value.label('triage'),
                        MedicalCamperVisit.medication_authorization.label('¿Quién autorizó el medicamento?'),
                        MedicalCamperVisit.event_description.label('Descripción del evento'),
                        MedicalCamperVisit.camp_restriction.label('Medidas durante el camp'),
                        MedicalCamperVisit.administered_medications.label('Tratamiento'),
                        MedicalCamperVisit.medical_monitoring.label('Seguimiento médico'),
                        MedicalCamperVisit.send_in_email.label('Notificar a los padres'),
                        MedicalCamperVisit.comment.label('Comentario'),
                        MedicalCamperVisit.initial_visit_id.label('medical_camper_visit'),
                        MedicalCamperVisit.medical_comment.label('Comentario interno'),
                        MedicalCamperVisit.additional_photo.label('Foto adicional')
                     
                     )
                      .select_from(MedicalCamperVisit)
                      .join(Camper, MedicalCamperVisit.camper_id == Camper.id)
                      .join(Constant, Constant.id == MedicalCamperVisit.triage)
                      .filter(MedicalCamperVisit.camp_id == camp_id)
             )
    medical_visits = db.execute(query)
    medical_visits = medical_visits.mappings().all()

    medical_visits_report = []
   
    for visit in medical_visits:
        
        visit_dict = dict(visit)
        
        visit_dict["Foto adicional"] = f"{BACKEND_DEV_URL}/{visit_dict['Foto adicional']}" if visit_dict['Foto adicional'] else ""
        
        visit_dict["Notificar a los padres"] = "Sí" if visit_dict['Notificar a los padres'] else "No"
        
        
        if visit.medical_camper_visit is not None:
            current_medical_visit = next(((medical_visit) for medical_visit in medical_visits if medical_visit.medical_camper_visit == visit.medical_camper_visit),None)
            visit_dict["Consulta de seguimiento"] = f"(seguimiento) - {current_medical_visit.Diagnostico}"
        else:
            visit_dict["Consulta de seguimiento"] = "Primera visita"
        medical_visits_report.append(visit_dict)                   
    
    return medical_visits_report


def get_camp_gnl_staff_report(db: Session, camp_id: int):
    
    
    query = (db.query(Staff.id,
                      Staff.name,
                      Staff.lastname_father,
                      Staff.lastname_mother,
                      Constant.value.label('gender'),
                      User.email.label("email"),
                      Staff.curp,
                      Staff.rfc,
                      Staff.cellphone,
                      Staff.home_phone,
                      Staff.birthday,
                      Staff.affliction, 
                      Staff.blood_type,
                      Staff.drug_allergies,
                      Staff.other_allergies,
                      Staff.nocturnal_disorders,
                      Staff.phobias,
                      Staff.drugs,
                      Staff.prohibited_foods,
                      Staff.bio,
                      Staff.coordinator,
                      Staff.facebook,
                      Staff.staff_contact_name,
                      Staff.staff_contact_relation,
                      Staff.staff_contact_homephone,
                      Staff.staff_contact_cellphone,
                      ).select_from(StaffInCamp)
             .join(Staff, Staff.id == StaffInCamp.staff_id)
             .join(Constant, Constant.id == Staff.gender_id)
             .join(User, Staff.login_id == User.id)
             .filter(and_(StaffInCamp.camp_id == camp_id, StaffInCamp.confirmed_staff == True)))
    staffs = db.execute(query)
    staffs = staffs.mappings().all()
    
    
    staffs_report = []
   
    for staff in staffs:
        staff_dict = dict(staff)

        staff_vaccines = get_staff_all_vaccines_by_staff_id(db, staff.id)
        staff_food_restriction = get_all_staff_food_restriction_by_id(db, staff.id)
        
        for food_restriction in staff_food_restriction:
            print(food_restriction)
            staff_dict[food_restriction["name"]] = food_restriction["is_active"]
        
        for vaccine in staff_vaccines:
            staff_dict[vaccine["name"]] = vaccine["is_active"]
            
        staffs_report.append(staff_dict)
       
    return staffs_report


def get_all_camp(db: Session, pagination: Pagination):
    order = desc if pagination.order == SortEnum.DESC else asc

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
            Camp.show_mercadopago_button,
            Camp.recommended_payment_dates
        ).select_from(Camp)
        .order_by(order(Camp.name))
        .limit(pagination.perPage)
        .offset((pagination.offset))
    )
    data = db.execute(query)
    data = data.mappings().all()
    rows_count = db.query(func.count(Camp.id)).select_from(Camp).scalar()    
    pages = get_number_of_pages(rows_count, pagination.perPage)

    return  {
        "pages": pages,
        "items": data,
        "total": rows_count
    }
    
    

    

def get_all_active_camp(db: Session, pagination):
    camps = []
    order = desc if pagination.order == SortEnum.DESC else asc
    
    query = (select(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.public_price.label("camp_public_price"),
            Camp.show_payment_parent.label("camp_show_payment_parent"),
            Location.name.label("location_name"),
            School.name.label("school_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Currency.name.label("camp_currency_name"),
            Currency.symbol.label("camp_currency_symbol"),
            Currency.acronyms.label("camp_currency_acronym"),
            Camp.photo_password
        
        )
        .join(Location, Location.id == Camp.location_id)
        .join(School, School.id == Camp.school_id)
        .join(Currency, Currency.id == Camp.currency_id)
        .filter(Camp.active==True and Camp.start >= date.today())
        .order_by(order(Camp.created_at))
        .limit(pagination.perPage)
        .offset((pagination.offset))
    )
    data = db.execute(query)
    data = data.mappings().all()
    rows_count = db.query(func.count(Camp.id)).select_from(Camp).join(Location, Location.id == Camp.location_id).join(Currency, Currency.id == Camp.currency_id).filter(Camp.active==True and Camp.start >= date.today()).scalar()    
    pages = get_number_of_pages(rows_count, pagination.perPage)
    
    for row in data:
        records = get_records_for_camp(db, row.camp_id)
        row = dict(row)
        row["records"] = records
        camps.append(row)

    return {
        "pages": pages,
        "items": camps,
        "total": rows_count
    }


def search_all_active_camp(db: Session, pagination, name, location, school):
    order = desc if pagination.order == SortEnum.DESC else asc
    camps = []
    db.execute(text('SET pg_trgm.similarity_threshold = 0.2'))
    query = (select(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.public_price.label("camp_public_price"),
            Camp.show_payment_parent.label("camp_show_payment_parent"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Camp.photo_password,
            Currency.name.label("camp_currency_name"),
            Currency.symbol.label("camp_currency_symbol"),
            Currency.acronyms.label("camp_currency_acronym"),
            Location.name.label("location_name"),
            School.name.label("school_name")
        )
        .join(Location, Location.id == Camp.location_id)
        .join(School, School.id == Camp.school_id)
        .join(Currency, Currency.id == Camp.currency_id)
        .filter(Camp.active==True)
        .filter(
            or_(
                Camp.name.op('%')(name),
                School.name.op('%')(school),
                Location.name.op('%')(location),
        ))
        .order_by(        
            func.similarity(Camp.name, name).desc(),
            func.similarity(School.name, school).desc(),
            func.similarity(Location.name, location).desc()
        )
        .limit(pagination.perPage)
        .offset((pagination.offset))
    )
    data = db.execute(query)
    data = data.mappings().all()
    rows_count = (
        db.query(func.count(Camp.id)).select_from(Camp).join(Location, Location.id == Camp.location_id).join(School, School.id == Camp.school_id).join(Currency, Currency.id == Camp.currency_id).filter(Camp.active==True)
        .filter(
            or_(
                Camp.name.op('%')(name),
                School.name.op('%')(school),
                Location.name.op('%')(location),
        )).scalar()
        )    
    pages = get_number_of_pages(rows_count, pagination.perPage)
    
    for row in data:
        records = get_records_for_camp(db, row.camp_id)
        row = dict(row)
        row["records"] = records
        camps.append(row)

    return {
        "pages": pages,
        "items": camps,
        "total": rows_count
    }



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


def get_camp_staff_by_camp_id(db: Session, camp_id: int):
    query = db.query( Camp.id,
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
                     Camp.location_id,
                     Camp.school_id,
                     Currency.name.label("camp_currency_name"),
                     Currency.symbol.label("camp_currency_symbol"),
                     Currency.acronyms.label("camp_currency_acronyms"),
                     Camp.recommended_payment_dates,
                     Camp.show_mercadopago_button,
                     Camp.created_at,
                     Camp.updated_at
                     ).select_from(Camp).join(Currency, Currency.id == Camp.currency_id).filter(Camp.id == camp_id)
    
    data = db.execute(query)
    data = data.mappings().first()
    return data


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
    campers_record = get_campers_for_module_count(db, camp_id)
    staff_available_record = get_staff_volunteer_in_camp_count(db, camp_id)
    staff_record = get_staff_in_camp_count(db, camp_id)

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
    query = (db.query(School.id.label('school_id'), School.name, School.email, School.contact_second_email, School.contact_third_email )
             .join(Camp, Camp.school_id == School.id).filter(Camp.id == camp_id)
             )
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


