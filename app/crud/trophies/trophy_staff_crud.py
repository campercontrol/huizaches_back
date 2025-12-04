import os
from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.trophies import TrophyStaff, Trophy, TrophySeason
from schema.trophies.trophy_schema import TrophyStaffCreate, TrophyStaffModify


TROPHY_TYPE_CERTIFICATION_ID = int(os.getenv("TROPHY_TYPE_CERTIFICATION_ID"))
TROPHY_TYPE_ACKNOWLEDGEMENT_ID = int(os.getenv("TROPHY_TYPE_ACKNOWLEDGEMENT_ID"))



def get_all_trophy_staff(db: Session):
    rows = db.query(TrophyStaff).all()
    return rows


def get_all_trophy_staff_id_name(db: Session):
    rows = db.query(TrophyStaff.id, TrophyStaff.name).all()
    return db_mapping_rows_to_dict(rows)


def get_trophy_staff_by_id(db: Session, trophy_staff_id: int):
    return (
        db.query(TrophyStaff)
        .filter_by(
            id=trophy_staff_id,
        )
        .first()
    )


def create_new_trophy_staff(db: Session, new_trophy_staff: TrophyStaffCreate):
    db_trophy_staff = None
    try:
        db_trophy_staff = TrophyStaff(**new_trophy_staff.dict())
        db.add(db_trophy_staff)
        db.commit()
        db.refresh(db_trophy_staff)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_trophy_staff = None
        return db_trophy_staff
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_trophy_staff


def update_trophy_staff_by_id(
    db: Session, trophy_staff_id: int, modify_trophy_staff: TrophyStaffModify
):
    rows_updated = (
        db.query(TrophyStaff)
        .filter_by(id=trophy_staff_id)
        .update(modify_trophy_staff, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def delete_trophy_staff(db: Session, trophy_staff_id: int):
    trophy_staff = (
        db.query(TrophyStaff).filter(TrophyStaff.id == trophy_staff_id).first()
    )
    db.delete(trophy_staff)
    db.commit()
    return {"status": True}


def get_trophy_by_staff(db: Session, staff_id: int):
    trophy_staff = db.query(TrophyStaff).filter(TrophyStaff.staff_id == staff_id).all()

    return {"trophies": trophy_staff}


def get_trophy_record_by_staff(db: Session, staff_id: int):
    trophy_staff_cert = (
        db.query(TrophyStaff)
        .join(TrophySeason, TrophySeason.id == TrophyStaff.trophy_season_id)
        .join(Trophy, Trophy.id == TrophySeason.trophy_id)
        .filter(and_(TrophyStaff.staff_id == staff_id, Trophy.trophy_type == TROPHY_TYPE_CERTIFICATION_ID))
        .count()
    )

    trophy_staff_cong = (
        db.query(TrophyStaff)
        .join(TrophySeason, TrophySeason.id == TrophyStaff.trophy_season_id)
        .join(Trophy, Trophy.id == TrophySeason.trophy_id)
        .filter(and_(TrophyStaff.staff_id == staff_id, Trophy.trophy_type == TROPHY_TYPE_ACKNOWLEDGEMENT_ID))
        .count()
    )
    
    
    return {
        "trophy_staff_cert" : trophy_staff_cert,
        "trophy_staff_cong" : trophy_staff_cong
    }
def get_all_staff_trophies(db: Session, staff_id: int):
    # query = db.query(Trophy.name).join(TrophySeason, TrophySeason.trophy_id == Trophy.id).join(TrophySeason, TrophyStaff.trophy_season_id == TrophySeason.id).filter(TrophyStaff.staff_id == staff_id)
    query = db.query(Trophy.name).join(TrophySeason, Trophy.id == TrophySeason.trophy_id).join(TrophyStaff, TrophySeason.id == TrophyStaff.trophy_season_id).filter(TrophyStaff.staff_id == staff_id)

    data = db.execute(query)
    data = data.mappings().all()
    return data