from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from model.catalogs import Currency
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_currency(db):
    rows = db.query(Currency).all()
    return rows

def get_currency_by_uuid(db, currency_id):
    return (
        db.query(Currency)
        .filter_by(
            id=currency_id,
        )
        .first()
    )


def create_new_currency(db, new_currency):
    db_currency = None
    try:
        db_currency = Currency(
            id=new_currency.id,
            name=new_currency.name,
            symbol=new_currency.symbol,
            acronyms=new_currency.acronyms,
            created_at=new_currency.created_at,
        )
        db.add(db_currency)
        db.commit()
        db.refresh(db_currency)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_currency = None
        return db_currency
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_currency


def update_currency_by_id(db, currency_id, modify_currency):
    rows_updated = (
        db.query(Currency).filter_by(id=currency_id).update(modify_currency, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def delete_currency(db: Session, currency_id:int):
    currency = db.query(Currency).filter(Currency.id==currency_id).first()
    db.delete(currency)
    db.commit()
    return {"status" : True}