from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.payments import PaymentMethod
from model.campers import Camper
from model.camps import Camp


from schema.payments.payment_method_schema import (
    PaymentMethodCreate,
    PaymentMethodModify,
)


def get_all_payment_method(db):
    rows = db.query(PaymentMethod).all()
    return rows


def get_payment_method_by_id(db, payment_method_id: int):
    return (
        db.query(PaymentMethod)
        .filter_by(
            id=payment_method_id,
        )
        .first()
    )


def create_new_payment_method(db, new_payment_method: PaymentMethodCreate):
    db_payment_method = None
    try:
        db_payment_method = PaymentMethod(**new_payment_method.dict())
        db.add(db_payment_method)
        db.commit()
        db.refresh(db_payment_method)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_payment_method = None
        return db_payment_method
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_payment_method


def update_payment_method_by_id(db, payment_method_id: int, modify_payment_method: PaymentMethodModify):
    rows_updated = (
        db.query(PaymentMethod)
        .filter_by(id=payment_method_id)
        .update(modify_payment_method, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

