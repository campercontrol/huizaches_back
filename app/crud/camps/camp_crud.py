from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import Camp
from schema.camps.camp_schema import CampCreate, CampModify

def get_all_camp(db: Session):
    rows = db.query(Camp).all()
    return rows

def get_all_active_camp(db: Session):
    rows = db.query(Camp).filter_by(active=True).all()
    return rows

def get_all_active_next_camp(db:Session):
    rows = db.query(Camp).filter(and_(db.camps_camp.active==True, db.camps_camp.start>=date.today())).all()
    return rows


#def get_all_camp_for_camper(school_id:int, db:Session):
#    rows = db.query(Camp).filter_by(school_id=school_id, active=True, start=datetime.now).all()
#    return rows

def get_camp_by_id(db:Session, camp_id: int):
    return(db.query(Camp).filter_by(id=camp_id).first())

def create_new_camp(db:Session, new_camp:CampCreate):
    db_camp = None
    try:
        db_camp= Camp(**new_camp.dict())
        db.add(db_camp)
        db.commit()
        db.refresh(db_camp)
    except SQLAlchemyError as e:
        print("#========================#")
        print(e)
        print("#========================#")
        db_camp = None
        return db_camp
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camp


def update_camp_by_id(db:Session, camp_id:int, modify_camp: CampModify):
    rows_updated= (
        db.query(Camp)
        .filter_by(id=camp_id)
        .update(modify_camp, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated