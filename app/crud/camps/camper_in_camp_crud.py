from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import CamperInCamp, Camp, Location
from model.catalogs import Constant
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


def get_subscribe_by_camper(db: Session, camper_id: int):
    
    rows = (
        db.query(
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
            CamperInCamp.payment_balance.label("camper_payment_balance"),
        )
        .join(Camp, CamperInCamp.camp_id == Camp.id)
        .join(Constant, CamperInCamp.status == Constant.id)
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.status == 36,
                Camp.active == True,
                Camp.start >= date.today(),
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_cancelled_by_camper(db:Session, camper_id:int):
    rows = (
        db.query(
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
            CamperInCamp.payment_balance.label("camper_payment_balance"),
        )
        .join(Camp, CamperInCamp.camp_id == Camp.id)
        .join(Constant, CamperInCamp.status == Constant.id)
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.status == 37,
                Camp.active == True,
                Camp.start >= date.today(),
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_past_subscribe_by_camper(db:Session, camper_id:int):
    rows = (
        db.query(
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
            CamperInCamp.payment_balance.label("camper_payment_balance"),
        )
        .join(Camp, CamperInCamp.camp_id == Camp.id)
        .join(Constant, CamperInCamp.status == Constant.id)
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.status == 36,
                Camp.active == True,
                Camp.start < date.today(),
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)