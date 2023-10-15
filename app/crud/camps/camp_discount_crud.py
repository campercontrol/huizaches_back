from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import CampDiscount
from model.camps import Camp

from schema.camps.camp_discount_schema import (
    CampDiscountCreate,
    CampDiscountModify,
)


def get_all_camp_discount(db):
    rows = db.query(CampDiscount).all()
    return rows


def get_camp_discount_by_id(db, camp_discount_id: int):
    return (
        db.query(CampDiscount)
        .filter_by(
            id=camp_discount_id,
        )
        .first()
    )


def create_new_camp_discount(db, new_camp_discount: CampDiscountCreate):
    db_camp_discount = None
    try:
        db_camp_discount = CampDiscount(**new_camp_discount.dict())
        db.add(db_camp_discount)
        db.commit()
        db.refresh(db_camp_discount)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camp_discount = None
        return db_camp_discount
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camp_discount


def update_camp_discount_by_id(db, camp_discount_id: int, modify_camp_discount: CampDiscountModify):
    rows_updated = (
        db.query(CampDiscount)
        .filter_by(id=camp_discount_id)
        .update(modify_camp_discount, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_camp_discount_by_camp(db, camp_id: int):
    rows = (
        db.query(CampDiscount)
        .join(Camp, Camp.id == camp_id)
        .filter(CampDiscount.camp_id == camp_id)
        .all()
    )
    return rows

def delete_camp_discount_camp(db, camp_discount_id:int):
    camp_discount_camp = db.query(CampDiscount).filter(CampDiscount.id==camp_discount_id).first()
    db.delete(camp_discount_camp)
    db.commit()
    return {"status": True}