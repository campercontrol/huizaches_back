from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.payments import Payment
from model.campers import Camper
from model.camps import Camp


from schema.payments.payment_schema import (
    PaymentCreate,
    PaymentModify,
)


def get_all_payment(db):
    rows = db.query(Payment).all()
    return rows


def get_payment_by_id(db, payment_id: int):
    return (
        db.query(Payment)
        .filter_by(
            id=payment_id,
        )
        .first()
    )


def create_new_payment(db, new_payment: PaymentCreate):
    db_payment = None
    try:
        db_payment = Payment(**new_payment.dict())
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_payment = None
        return db_payment
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_payment


def update_payment_by_id(db, payment_id: int, modify_payment: PaymentModify):
    rows_updated = (
        db.query(Payment)
        .filter_by(id=payment_id)
        .update(modify_payment, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_payment_by_camper_camp(db, camper_id: int, camp_id: int):
    rows = (
        db.query(Payment)
        .join(Camper, Camper.id == camper_id)
        .join(Camp, Camp.id== camp_id)
        .filter(and_(Payment.camper_id == camper_id, Payment.camp_id == camp_id))
        .all()
    )
    return rows
