from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.camps import Location
from schema.camps.location_schema import LocationCreate, LocationModify


def get_all_location(db: Session):
    rows = db.query(Location).all()
    return rows


def get_all_active_location_id_name(db: Session):
    rows = db.query(Location.id, Location.name).filter_by(active=True).all()
    return db_mapping_rows_to_dict(rows)


def get_location_by_uuid(db: Session, location_id: int):
    return (
        db.query(Location)
        .filter_by(
            id=location_id,
        )
        .first()
    )


def create_new_location(db: Session, new_location: LocationCreate):
    db_location = None
    try:
        db_location = Location(**new_location.dict())
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_location = None
        return db_location
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_location


def update_location_by_id(db: Session, location_id: int, modify_location: LocationModify):
    rows_updated = (
        db.query(Location)
        .filter_by(id=location_id)
        .update(modify_location, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
