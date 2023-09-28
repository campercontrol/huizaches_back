from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from model.catalogs import PaymentAccount
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_payment_account(db):
    rows = db.query(PaymentAccount).all()
    return rows

def get_payment_account_by_uuid(db, payment_account_id):
    return (
        db.query(PaymentAccount)
        .filter_by(
            id=payment_account_id,
        )
        .first()
    )


def create_new_payment_account(db, new_payment_account):
    db_payment_account = None
    try:
        db_payment_account = PaymentAccount(
            id=new_payment_account.id,
            name=new_payment_account.name,
            bank=new_payment_account.bank,
            account_number=new_payment_account.account_number,
            clabe_number=new_payment_account.clabe_number,
        )
        db.add(db_payment_account)
        db.commit()
        db.refresh(db_payment_account)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_payment_account = None
        return db_payment_account
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_payment_account


def update_payment_account_by_id(db, payment_account_id, modify_payment_account):
    rows_updated = (
        db.query(PaymentAccount).filter_by(id=payment_account_id).update(modify_payment_account, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def delete_payment_account(db: Session, payment_account_id:int):
    payment_account = db.query(PaymentAccount).filter(PaymentAccount.id==payment_account_id).first()
    db.delete(payment_account)
    db.commit()
    return {"status" : True}
