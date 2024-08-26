from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from utils.db import db_mapping_rows_to_dict
from fastapi import HTTPException
from model.medical.medical_camper_visit import MedicalCamperVisit
from model.catalogs.constant import Constant
from model.campers.camper import Camper
from schema.medical.camper_visit_schema import CamperVisitCreate


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

def create_new_camper_visit(db: Session, new_camper_visit: CamperVisitCreate):
    db_camper_visit = None
    try:
        db_camper_visit = MedicalCamperVisit(**new_camper_visit.dict())
        db.add(db_camper_visit)
        db.commit()
        db.refresh(db_camper_visit)
    except SQLAlchemyError as e:
        return {"status": 2, "detail": "Can not save de medical visit"}
    except Exception as ex:
        db.rollback()
        return {"status": 3, "detail": "Internal server error"}
    return {"status": 1, "detail": "medical visit created successfully"}
