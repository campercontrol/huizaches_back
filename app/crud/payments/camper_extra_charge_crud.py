from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.catalogs import Currency
from model.payments import CamperExtraCharge
from model.camps import CampExtraCharge

from schema.payments.camper_extra_charge_schema import (
    CamperExtraChargeCreate,
    CamperExtraChargeModify,
    CamperExtraChargeListCreate,
)

from crud.camps.camp_extra_charge_crud import get_extra_charge_by_camp


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


def create_new_camper_extra_charge(
    db, new_camper_extra_charge: CamperExtraChargeCreate
):
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


def update_camper_extra_charge_by_id(
    db, camper_extra_charge_id: int, modify_camper_extra_charge: CamperExtraChargeModify
):
    rows_updated = (
        db.query(CamperExtraCharge)
        .filter_by(id=camper_extra_charge_id)
        .update(modify_camper_extra_charge, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_extra_charge_by_camper_camp(db, camper_id: int, camp_id: int):
    query = (
            db.query(
                CampExtraCharge.id.label("extra_charge_id"),
                CampExtraCharge.name.label("extra_charge_name"),
                Currency.symbol.label("extra_charge_symbol"),
                CampExtraCharge.price.label("extra_charge_price"),
                CamperExtraCharge.is_selected.label("extra_selected"),
                CamperExtraCharge.id.label("camper_extra_charge_id")
            )
            .select_from(CamperExtraCharge)
            .join(
                CampExtraCharge, CampExtraCharge.id == CamperExtraCharge.extra_charge_id
            ).join(
                Currency, CampExtraCharge.currency_id == Currency.id
            )
            .filter(
                CamperExtraCharge.camper_id == camper_id,
                CampExtraCharge.camp_id == camp_id
            )
        )    
    extra_charges = db.execute(query)
    extra_charges = extra_charges.mappings().all()
    return extra_charges


def create_update_extra_charges(db, extra_charges: CamperExtraChargeListCreate):
    for extra_charge in extra_charges.extra_charges:
        row = (
            db.query(CamperExtraCharge)
            .join(
                CampExtraCharge, CampExtraCharge.id == CamperExtraCharge.extra_charge_id
            )
            .filter(
                CamperExtraCharge.extra_charge_id
                == getattr(extra_charge, "extra_charge_id")
            )
            .first()
        )

        if row:
            camper_schema = CamperExtraChargeModify(
                id=getattr(row, "id"),
                is_selected=getattr(extra_charge, "extra_selected"),
                camper_id=getattr(row, "camper_id"),
                extra_charge_id=getattr(row, "extra_charge_id"),
            )
            extra_c = update_camper_extra_charge_by_id(
                db, getattr(row, "id"), camper_schema.dict()
            )
        else:
            camper_schema = CamperExtraChargeCreate(
                is_selected=getattr(extra_charge, "extra_selected"),
                camper_id=getattr(extra_charge, "camper_id"),
                extra_charge_id=getattr(extra_charge, "extra_charge_id"),
            )
            extra_c = create_new_camper_extra_charge(db, camper_schema)

    return extra_c
