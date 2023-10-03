from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.trophies import TrophySeason
from schema.trophies.trophy_schema import TrophySeasonCreate, TrophySeasonModify

def get_all_trophy_season(db: Session):
    rows = db.query(TrophySeason).all()
    return rows


def get_all_trophy_season_id_name(db: Session):
    rows = db.query(TrophySeason.id, TrophySeason.name).all()
    return db_mapping_rows_to_dict(rows)


def get_trophy_season_by_id(db: Session, trophy_season_id: int):
    return (
        db.query(TrophySeason)
        .filter_by(
            id=trophy_season_id,
        )
        .first()
    )


def create_new_trophy_season(db: Session, new_trophy_season: TrophySeasonCreate):
    db_trophy_season = None
    try:
        db_trophy_season = TrophySeason(**new_trophy_season.dict())
        db.add(db_trophy_season)
        db.commit()
        db.refresh(db_trophy_season)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_trophy_season = None
        return db_trophy_season
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_trophy_season


def update_trophy_season_by_id(db: Session, trophy_season_id: int, modify_trophy_season: TrophySeasonModify):
    rows_updated = (
        db.query(TrophySeason)
        .filter_by(id=trophy_season_id)
        .update(modify_trophy_season, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def delete_trophy_season(db: Session, trophy_season_id:int):
    trophy_season = db.query(TrophySeason).filter(TrophySeason.id==trophy_season_id).first()
    db.delete(trophy_season)
    db.commit()
    return {"status" : True}
