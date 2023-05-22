from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.payments import CamperExtraCharge

from schema.payments.camper_extra_charge_schema import (
    CamperExtraChargeCreate,
    CamperExtraChargeModify,
)


def get_all_camper_extra_charge(db):
    rows = db.query(CamperExtraCharge).all()
    return rows


def get_camper_extra_charge_by_id(db, camper_extra_charge_id: int):
    return (
        db.query(CamperExtraCharge)
        .filter_by(
            id=camper_extra_charge_id,
        )
        .first()
    )


def create_new_camper_extra_charge(db, new_camper_extra_charge: CamperExtraChargeCreate):
    db_camper_extra_charge = None
    try:
        db_camper_extra_charge = CamperExtraCharge(**new_camper_extra_charge.dict())
        db.add(db_camper_extra_charge)
        db.commit()
        db.refresh(db_camper_extra_charge)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_extra_charge = None
        return db_camper_extra_charge
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_extra_charge


def update_camper_extra_charge_by_id(db, camper_extra_charge_id: int, modify_camper_extra_charge: CamperExtraChargeModify):
    rows_updated = (
        db.query(CamperExtraCharge)
        .filter_by(id=camper_extra_charge_id)
        .update(modify_camper_extra_charge, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

