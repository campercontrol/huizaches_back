from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.medical import MedicalStaffVisit
from model.catalogs import Constant

def staff_visit_triage_for_camp(db, staff_id: int, camp_id: int):
    staff_triages = (
        db.query(Constant.id, Constant.value)
        .select_from(MedicalStaffVisit)
        .join(Constant, Constant.id == MedicalStaffVisit.triage)
        .filter(
            and_(
                MedicalStaffVisit.staff_id == staff_id,
                MedicalStaffVisit.camp_id == camp_id,
            )
        )
        .all()
    )
    return staff_triages