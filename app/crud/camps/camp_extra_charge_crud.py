from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import CampExtraCharge
from model.camps import Camp

from schema.camps.camp_extra_charge_schema import (
    CampExtraChargeCreate,
    CampExtraChargeModify,
)


def get_all_extra_charge(db):
    rows = db.query(CampExtraCharge).all()
    return rows


def get_extra_charge_by_id(db, extra_charge_id: int):
    return (
        db.query(CampExtraCharge)
        .filter_by(
            id=extra_charge_id,
        )
        .first()
    )


def create_new_extra_charge(db, new_extra_charge: CampExtraChargeCreate):
    db_extra_charge = None
    try:
        db_extra_charge = CampExtraCharge(**new_extra_charge.dict())
        db.add(db_extra_charge)
        db.commit()
        db.refresh(db_extra_charge)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_extra_charge = None
        return db_extra_charge
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_extra_charge


def update_extra_charge_by_id(db, extra_charge_id: int, modify_extra_charge: CampExtraChargeModify):
    rows_updated = (
        db.query(CampExtraCharge)
        .filter_by(id=extra_charge_id)
        .update(modify_extra_charge, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_extra_charge_by_camp(db, camp_id: int):
    rows = (
        db.query(CampExtraCharge)
        .join(Camp, Camp.id == camp_id)
        .filter(CampExtraCharge.camp_id == camp_id)
        .all()
    )
    return rows

def delete_extra_charge_camp(db, extra_charge_id:int):
    extra_charge_camp = db.query(CampExtraCharge).filter(CampExtraCharge.id==extra_charge_id).first()
    db.delete(extra_charge_camp)
    db.commit()
    return {"status": True}