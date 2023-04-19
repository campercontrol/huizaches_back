from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.camps import CamperInCamp
from schema.camps.camper_in_camp_schema import (
    CamperInCampCreate,
    CamperInCampModify,
)


def get_all_camper_in_camp(db: Session):
    rows = db.query(CamperInCamp).all()
    return rows


def create_new_camper_in_camp(db: Session, new_camper_in_camp: CamperInCampCreate):
    db_camper_in_camp = None
    try:
        db_camper_in_camp = CamperInCamp(**new_camper_in_camp.dict())
        db.add(db_camper_in_camp)
        db.commit()
        db.refresh(db_camper_in_camp)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_in_camp = None
        return db_camper_in_camp
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_in_camp


def update_camper_in_camp_by_id(
    db: Session,
    camp_id: int,
    camper_id: int,
    modify_camper_in_camp: CamperInCampModify,
):
    print("######################################################")
    print(type(modify_camper_in_camp))
    rows_updated = (
        db.query(CamperInCamp)
        .filter_by(camp_id=camp_id, camper_id=camper_id)
        .update(modify_camper_in_camp, synchronize_session="fetch")
    )
    print(rows_updated)
    db.commit()
    return rows_updated
