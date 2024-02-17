from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.trophies import Trophy
from schema.trophies.trophy_schema import TrophyCreate, TrophyModify

def get_all_trophy(db: Session):
    rows = db.query(Trophy).all()
    return rows


def get_all_trophy_id_name(db: Session):
    rows = db.query(Trophy.id, Trophy.name).all()
    return db_mapping_rows_to_dict(rows)


def get_trophy_by_id(db: Session, trophy_id: int):
    return (
        db.query(Trophy)
        .filter_by(
            id=trophy_id,
        )
        .first()
    )


def create_new_trophy(db: Session, new_trophy: TrophyCreate):
    db_trophy = None
    try:
        db_trophy = Trophy(**new_trophy.dict())
        db.add(db_trophy)
        db.commit()
        db.refresh(db_trophy)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_trophy = None
        return db_trophy
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_trophy


def update_trophy_by_id(db: Session, trophy_id: int, modify_trophy: TrophyModify):
    rows_updated = (
        db.query(Trophy)
        .filter_by(id=trophy_id)
        .update(modify_trophy, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def delete_trophy(db: Session, trophy_id:int):
    trophy = db.query(Trophy).filter(Trophy.id==trophy_id).first()
    db.delete(trophy)
    db.commit()
    return {"status" : True}
