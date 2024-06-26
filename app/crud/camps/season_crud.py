from sqlalchemy import case, update
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
        if new_season["current"]:
            switch_current_to_false_stmt =  (
                update(Season)
                .where(Season.current == True)
                .values(current=False)
            )
        db.execute(switch_current_to_false_stmt)
        db_season = Season(**new_season)
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
        db_season = None
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_season


def update_season_by_id(db: Session, season_id: int, modify_season: SeasonModify):
    try: 
        if modify_season["current"]:
            switch_to_false_stmt =  (
                update(Season)
                .where(Season.current == True)
                .values(current=False)
            )
            db.execute(switch_to_false_stmt)
        rows_updated = (
            db.query(Season)
            .filter_by(id=season_id)
            .update(modify_season, synchronize_session="fetch")
        )
        db.commit()
    except Exception as ex:
        print(ex)
        return {"status": 3, "msg": "Internal Server Error"}
    
    return {"status": 1, "msg": "Season updated successfully"}

def delete_season(db: Session, season_id:int):
    season = db.query(Season).filter(Season.id==season_id).first()
    db.delete(season)
    db.commit()
    return {"status" : True}
