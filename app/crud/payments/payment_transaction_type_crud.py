from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.payments import PaymentTransactionType
from model.campers import Camper
from model.camps import Camp


from schema.payments.payment_transaction_type_schema import (
    PaymentTransactionTypeCreate,
    PaymentTransactionTypeModify,
)


def get_all_payment_transaction_type(db):
    rows = db.query(PaymentTransactionType).all()
    return rows


def get_payment_transaction_type_by_id(db, payment_transaction_type_id: int):
    return (
        db.query(PaymentTransactionType)
        .filter_by(
            id=payment_transaction_type_id,
        )
        .first()
    )


def create_new_payment_transaction_type(
    db, new_payment_transaction_type: PaymentTransactionTypeCreate
):
    db_payment_transaction_type = None
    try:
        db_payment_transaction_type = PaymentTransactionType(
            **new_payment_transaction_type.dict()
        )
        db.add(db_payment_transaction_type)
        db.commit()
        db.refresh(db_payment_transaction_type)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_payment_transaction_type = None
        return db_payment_transaction_type
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_payment_transaction_type


def update_payment_transaction_type_by_id(
    db,
    payment_transaction_type_id: int,
    modify_payment_transaction_type: PaymentTransactionTypeModify,
):
    rows_updated = (
        db.query(PaymentTransactionType)
        .filter_by(id=payment_transaction_type_id)
        .update(modify_payment_transaction_type, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
