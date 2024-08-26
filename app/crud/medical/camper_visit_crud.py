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
    initial_visit = aliased(MedicalCamperVisit)
    tracing_visit = aliased(MedicalCamperVisit)
    tracing_visit_query = (db.query(
                tracing_visit.id.label("tracing_visit_id"),
                tracing_visit.initial_visit_id.label("tracing_visit_initial_visit_id"),
                tracing_visit.diagnostic.label("tracing_visit_diagnostic"),
                tracing_visit.administered_medications.label("tracing_visit_administered_medication"),
                tracing_visit.doctor.label("tracing_visit_doctor"),
                tracing_visit.attention_date.label("tracing_visit_attention_date"),
                tracing_visit.attention_time.label("tracing_visit_attention_time"),
                tracing_visit.description.label("tracing_visit_description"),
                tracing_visit.attention_time.label("tracing_visit_attention_time"),
                Constant.value,
                tracing_visit.medication_authorization.label("tracing_visit_medical_authorization"),
                tracing_visit.event_description.label("tracing_visit_event_description"),
                tracing_visit.camp_restriction.label("tracing_visit_camp_restriction"),
                tracing_visit.medical_monitoring.label("tracing_visit_medical_monitoring"),
                tracing_visit.comment.label("tracing_visit_comment"),
                tracing_visit.medical_comment.label("tracing_visit_medical_comment"),
                tracing_visit.send_in_email.label("tracing_visit_send_in_email"),
                tracing_visit.already_sent.label("tracing_visit_already_sent"),
                tracing_visit.camper_id.label("tracing_visit_camper_id"))
                .select_from(initial_visit)
                .join(tracing_visit, initial_visit.id == tracing_visit.initial_visit_id, isouter=True)
                .join(Constant, initial_visit.triage == Constant.id)
                .where(and_(initial_visit.initial_visit_id.is_(None), initial_visit.camper_id == camper_id, initial_visit.camp_id == camp_id)))
    
    initial_visit_query = (
        db.query(MedicalCamperVisit, Constant.value)
        .select_from(MedicalCamperVisit)
        .join(Constant, Constant.id == MedicalCamperVisit.triage)
        .filter(
            and_(
                MedicalCamperVisit.camper_id == camper_id,
                MedicalCamperVisit.initial_visit_id.is_(None),
                MedicalCamperVisit.camp_id == camp_id,
            )
        )
    )
    data_tracing_visit = db.execute(tracing_visit_query)
    data_initial_visit = db.execute(initial_visit_query)
    
    data_tracing_visit = data_tracing_visit.mappings().all() 
    data_initial_visit = data_initial_visit.mappings().first()

    if(data_initial_visit):
        initial_visit_dict = dict(data_initial_visit)
        initial_visit_dict["tracing_visits"] = data_tracing_visit
        return initial_visit_dict
    return data_initial_visit

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
