import os
from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from utils.db import db_mapping_rows_to_dict
from helper.mailing_helpers import send_mail_template_medical_visit
from fastapi import HTTPException
from model.medical.medical_camper_visit import MedicalCamperVisit
from model.catalogs.constant import Constant
from model.campers.camper import Camper
from schema.medical.camper_visit_schema import CamperVisitCreate, CamperVisitModify
from crud.mailings.mailing_crud import get_camper_info_mailing, get_camp_info_by_id_mailing, get_admin_users_for_mailing
from crud.campers.parent_crud import get_parent_by_camper_id, get_second_tutor_by_camper_id


BASE_URL = os.getenv("BACKEND_PROD_URL")
def camper_visit_triage_for_camp(db, camper_id: int, camp_id: int):
    camper_triages = (
        db.query(
            MedicalCamperVisit.id,
            Constant.value,
            MedicalCamperVisit.medical_tracing,
            MedicalCamperVisit.initial_visit_id,
        )
        .select_from(MedicalCamperVisit)
        .join(Constant, Constant.id == MedicalCamperVisit.triage)
        .filter(
            and_(
                MedicalCamperVisit.camper_id == camper_id,
                MedicalCamperVisit.camp_id == camp_id,
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(camper_triages)


# def camper_visit_for_camp(db, camper_id: int, camp_id: int):
#     camper_visits = (
#         db.query(MedicalCamperVisit, Constant.value)
#         .select_from(MedicalCamperVisit)
#         .join(Constant, Constant.id == MedicalCamperVisit.triage)
#         .filter(
#             and_(
#                 MedicalCamperVisit.camper_id == camper_id,
#                 MedicalCamperVisit.camp_id == camp_id,
#             )
#         )
#         .all()
#     )
#     return db_mapping_rows_to_dict(camper_visits)

def camper_visit_for_camp(db, camper_id: int, camp_id: int):
        
    initial_visits_query = (
        db.query(
                MedicalCamperVisit.id,
                MedicalCamperVisit.initial_visit_id,
                MedicalCamperVisit.diagnostic,
                MedicalCamperVisit.administered_medications,
                MedicalCamperVisit.doctor,
                MedicalCamperVisit.attention_date,
                MedicalCamperVisit.attention_time,
                MedicalCamperVisit.description,
                MedicalCamperVisit.attention_time,
                Constant.value.label("triage"),
                MedicalCamperVisit.medication_authorization,
                MedicalCamperVisit.event_description,
                MedicalCamperVisit.camp_restriction,
                MedicalCamperVisit.medical_monitoring,
                MedicalCamperVisit.comment,               
                MedicalCamperVisit.medical_comment,
                MedicalCamperVisit.send_in_email,
                MedicalCamperVisit.already_sent,
                MedicalCamperVisit.additional_photo,
                MedicalCamperVisit.camper_id)
        .select_from(MedicalCamperVisit)
        .join(Constant, Constant.id == MedicalCamperVisit.triage)
        .where(
            and_(
                MedicalCamperVisit.camper_id == camper_id,
                MedicalCamperVisit.initial_visit_id.is_(None),
                MedicalCamperVisit.camp_id == camp_id,
            )
        )
    )
    data_initial_visits = db.execute(initial_visits_query)
    data_initial_visits = data_initial_visits.mappings().all()
    
    camper_all_visits = []
    
    for data_initial_visit in data_initial_visits:    
        tracing_visit_query = (db.query(
            MedicalCamperVisit.id,
            MedicalCamperVisit.initial_visit_id,
            MedicalCamperVisit.diagnostic,
            MedicalCamperVisit.administered_medications,
            MedicalCamperVisit.doctor,
            MedicalCamperVisit.attention_date,
            MedicalCamperVisit.attention_time,
            MedicalCamperVisit.description,
            MedicalCamperVisit.attention_time,
            Constant.value.label("triage"),
            MedicalCamperVisit.medication_authorization,
            MedicalCamperVisit.event_description,
            MedicalCamperVisit.camp_restriction,
            MedicalCamperVisit.medical_monitoring,
            MedicalCamperVisit.comment,
            MedicalCamperVisit.medical_comment,
            MedicalCamperVisit.send_in_email,
            MedicalCamperVisit.already_sent,
            MedicalCamperVisit.additional_photo,
            MedicalCamperVisit.camper_id)
            .select_from(MedicalCamperVisit)
            .join(Constant, Constant.id == MedicalCamperVisit.triage)
            .where(
                and_(
                    MedicalCamperVisit.camper_id == camper_id,
                    MedicalCamperVisit.initial_visit_id == data_initial_visit.id, 
                    MedicalCamperVisit.camp_id == camp_id
                )
            )).order_by(MedicalCamperVisit.attention_date)   
        data_tracing_visit = db.execute(tracing_visit_query)
        data_tracing_visit = data_tracing_visit.mappings().all() 
        
        initial_visit_dict = dict(data_initial_visit)
        initial_visit_dict["tracing_visits"] = data_tracing_visit  
        camper_all_visits.append(initial_visit_dict)
    
    return camper_all_visits


def get_camper_medical_visit_by_id (db: Session, camper_medical_visit_id: int):
    medical_visit_query = (
        db.query(
            MedicalCamperVisit.medical_tracing,
            MedicalCamperVisit.event_description,
            MedicalCamperVisit.already_sent,
            MedicalCamperVisit.doctor,
            MedicalCamperVisit.camp_restriction,
            MedicalCamperVisit.camper_id,
            MedicalCamperVisit.camp_id,
            MedicalCamperVisit.attention_date,
            MedicalCamperVisit.administered_medications,
            MedicalCamperVisit.attention_time,
            MedicalCamperVisit.medical_monitoring,
            MedicalCamperVisit.initial_visit_id,
            MedicalCamperVisit.diagnostic,
            MedicalCamperVisit.comment,
            MedicalCamperVisit.created_at,
            MedicalCamperVisit.description,
            MedicalCamperVisit.medical_comment,
            MedicalCamperVisit.updated_at,
            MedicalCamperVisit.id,
            MedicalCamperVisit.send_in_email,
            MedicalCamperVisit.medication_authorization,
            MedicalCamperVisit.additional_photo,
            Constant.value.label('triage')).select_from(MedicalCamperVisit).join(Constant, Constant.id == MedicalCamperVisit.triage).filter(MedicalCamperVisit.id == camper_medical_visit_id)
    
    )
    
    medical_visit = db.execute(medical_visit_query)
    medical_visit = medical_visit.mappings().first()
    return medical_visit
    
def update_medical_camper_visit(db: Session, camper_visit_update: CamperVisitModify, visit_id: int):
    data = camper_visit_update.dict(exclude_unset=True)
    try:
        updated_data = (
            db.query(MedicalCamperVisit)
            .filter(MedicalCamperVisit.id == visit_id)
            .update(data, synchronize_session="fetch")
        )
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error updating camper visit: {e}")
        raise HTTPException(status_code=500, detail={"status": 3, "detail": "Internal server error"})
    return updated_data

def create_new_camper_visit(db: Session, new_camper_visit: CamperVisitCreate):
    
    db_camper_visit = None
    try:
        
        
        db_camper_visit = MedicalCamperVisit(**new_camper_visit.dict())
        db_camper_visit.medication_authorization = case(
            {
                "1": "Preautorización en sistema de registro",
                "2": "Se contacta a tutores",
                "3": "Por parte de la Escuela / Maestras",
                "4": "Por parte de Camper Control (In Loco Parentis)",
                "5": "No se administraron medicamentos",
            },
            value=new_camper_visit.medication_authorization,
        )
        parent_table_template_id = 1985
        staff_table_template_id = 2000
        
        
        db.add(db_camper_visit)
        db.commit()
        db.refresh(db_camper_visit)
        additional_photo = f"{BASE_URL}/{new_camper_visit.additional_photo}"
        if new_camper_visit.send_in_email:
            
            camper_data = get_camper_info_mailing(db, new_camper_visit.camper_id)
            camp_data = get_camp_info_by_id_mailing(db, new_camper_visit.camp_id)
            first_parent = get_parent_by_camper_id(db, new_camper_visit.camper_id)
            second_parent = get_second_tutor_by_camper_id(db, new_camper_visit.camper_id)
            admin_users = get_admin_users_for_mailing(db)    
            medical_visit_parent_template = 1984
            medical_visit_admin_template = 1983
            medical_visit = get_camper_medical_visit_by_id(db, db_camper_visit.id)
            
            
            first_parent_context = {
                "camper": camper_data,
                "user": first_parent,
                "camp": camp_data,
                "medical_visit": medical_visit,
                "additional_photo": additional_photo
            }
            second_parent_context = {
                "camper": camper_data,
                "user": second_parent,
                "camp": camp_data,
                "medical_visit": medical_visit,
                "additional_photo": additional_photo
            }
            send_mail_template_medical_visit(db, first_parent["email"], medical_visit_parent_template, first_parent_context, parent_table_template_id)    
            send_mail_template_medical_visit(db, second_parent["email"], medical_visit_parent_template, second_parent_context, parent_table_template_id)   
            
            for admin_user in admin_users:
                admin_user_context = {
                    "camper": camper_data,
                    "user": admin_user,
                    "camp": camp_data,
                    "medical_visit": medical_visit,
                    "additional_photo": additional_photo
                }  
                send_mail_template_medical_visit(db, admin_user['email'], medical_visit_admin_template, admin_user_context, staff_table_template_id)
            db_camper_visit.already_sent = True
            db.commit()    
            
                      
    except SQLAlchemyError as e:
        db.rollback()
        print(e)
        return {"status": 2, "detail": "Can not save de medical visit"}
    except Exception as ex:
        db.rollback()
        print(ex)
        return {"status": 3, "detail": "Internal server error"}
    return {"status": 1, "detail": "medical visit created successfully"}


