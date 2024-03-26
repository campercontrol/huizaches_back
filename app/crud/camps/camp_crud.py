from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import Camp, Location, CamperInCamp, StaffInCamp
from model.campers import Camper
from schema.camps.camp_schema import CampCreate, CampModify

from crud.camps.camper_in_camp_crud import get_campers_for_module
from crud.camps.staff_in_camp_crud import get_staff_volunteer_in_camp, get_staff_in_camp


def get_all_camp(db: Session):
    rows = db.query(Camp).all()
    return rows


def get_all_active_camp(db: Session):
    camps = []
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.public_price.label("camp_public_price"),
            Camp.show_payment_parent.label("camp_show_payment_parent"),
            Location.name.label("location_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end")
        )
        .join(Location, Location.id == Camp.location_id)
        .filter(Camp.active==True)
        .all()
    )
    for row in db_mapping_rows_to_dict(rows):
        records = get_records_for_camp(db, row.camp_id)
        row = dict(row)
        row["records"] = records
        camps.append(row)

    return camps


def get_school_camp_for_camper(db: Session, camper_id: int):
    school_id = db.query(Camper.school_id).filter_by(id=camper_id).first()
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
        )
        .join(Location, Location.id == Camp.location_id)
        .filter(
            and_(
                Camp.general_camp == False,
                Camp.school_id == school_id[0],
                Camp.active == True,
                Camp.start >= date.today(),
                Camp.registration == True,
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_summer_camp_for_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
        )
        .join(Location, Location.id == Camp.location_id)
        .filter(
            and_(
                Camp.general_camp == True,
                Camp.active == True,
                Camp.start >= date.today(),
                Camp.registration == True,
            )
        )
    )
    return db_mapping_rows_to_dict(rows)


def get_camp_by_id(db: Session, camp_id: int):
    return db.query(Camp).filter_by(id=camp_id).first()


def create_new_camp(db: Session, new_camp: CampCreate):
    db_camp = None
    try:
        db_camp = Camp(**new_camp.dict())
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


def update_camp_by_id(db: Session, camp_id: int, modify_camp: CampModify):
    rows_updated = (
        db.query(Camp)
        .filter_by(id=camp_id)
        .update(modify_camp, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def delete_camp(db: Session, camp_id: int):
    camp = db.query(Camp).filter(Camp.id == camp_id).first()
    db.delete(camp)
    db.commit()
    return {"status": True}


def get_records_for_camp(db: Session, camp_id: int):
    campers_record = len(get_campers_for_module(db, camp_id))
    staff_available_record = len(get_staff_volunteer_in_camp(db, camp_id))
    staff_record = len(get_staff_in_camp(db, camp_id))

    return {
        "campers_recod": campers_record,
        "staff_available_record": staff_available_record,
        "staff_record": staff_record,
    }


# 2


def get_camp_by_search(db: Session, search: str):
    camps = (
        db.query(Camp.id.label("camp_id"), Camp.name.label("camp_name"))
        .filter(Camp.name.ilike(r"%{}%".format(search)))
        .all()
    )

    if not camps:
        return "Data not found"

    return db_mapping_rows_to_dict(camps)


def get_camp_by_search(db: Session, search: str):
    camps = (
        db.query(Camp.id.label("camp_id"), Camp.name.label("camp_name"))
        .filter(Camp.name.ilike(r"%{}%".format(search)))
        .all()
    )

    if not camps:
        return "Data not found"

    return db_mapping_rows_to_dict(camps)
