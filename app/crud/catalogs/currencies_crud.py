from sqlalchemy.exc import SQLAlchemyError

from model.catalogs import Currencies
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_currencies(db):
    rows = db.query(Currencies).all()
    return rows

def get_currencies_by_uuid(db, currencies_id):
    return (
        db.query(Currencies)
        .filter_by(
            id=currencies_id,
        )
        .first()
    )


def create_new_currencies(db, new_currencies):
    db_currencies = None
    try:
        db_currencies = Currencies(
            name_currency=new_currencies.name_currency
        )
        db.add(db_currencies)
        db.commit()
        db.refresh(db_currencies)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_currencies = None
        return db_currencies
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_currencies


def update_currencies_by_id(db, currencies_id, modify_currencies):
    rows_updated = (
        db.query(Currencies).filter_by(id=currencies_id).update(modify_currencies, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
