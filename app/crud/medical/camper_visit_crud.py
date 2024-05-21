from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from fastapi import HTTPException
from model.medical.medical_camper_visit import MedicalCamperVisit
from model.catalogs.constant import Constant
from model.campers.camper import Camper
from schema.medical.camper_visit_schema import CamperVisitCreate


def camper_visit_triage_for_camp(db, camper_id: int, camp_id: int):
    camper_triages = (
        db.query(
            Constant.id,
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


def camper_visit_for_camp(db, camper_id: int, camp_id: int):
    camper_visits = (
        db.query(MedicalCamperVisit, Constant.value)
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
    return db_mapping_rows_to_dict(camper_visits)


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
