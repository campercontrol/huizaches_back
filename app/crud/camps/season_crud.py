from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.camps import Season
from schema.camps.season_schema import SeasonCreate, SeasonModify

def get_all_season(db: Session):
    rows = db.query(Season).all()
    return rows


def get_all_season_id_name(db: Session):
    rows = db.query(Season.id, Season.name).all()
    return db_mapping_rows_to_dict(rows)


def get_season_by_id(db: Session, season_id: int):
    return (
        db.query(Season)
        .filter_by(
            id=season_id,
        )
        .first()
    )


def create_new_season(db: Session, new_season: SeasonCreate):
    db_season = None
    try:
        db_season = Season(**new_season.dict())
        db.add(db_season)
        db.commit()
        db.refresh(db_season)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_season = None
        return db_season
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_season


def update_season_by_id(db: Session, season_id: int, modify_season: SeasonModify):
    rows_updated = (
        db.query(Season)
        .filter_by(id=season_id)
        .update(modify_season, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def delete_season(db: Session, season_id:int):
    season = db.query(Season).filter(Season.id==season_id).first()
    db.delete(season)
    db.commit()
    return {"status" : True}
