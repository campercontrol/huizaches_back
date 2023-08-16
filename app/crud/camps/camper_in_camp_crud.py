from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import CamperInCamp, Camp, Location
from model.campers import Camper, CamperRecord, Parent
from model.catalogs import Constant
from model.user import User
from schema.camps.camper_in_camp_schema import (
    CamperInCampCreate,
    CamperInCampModify,
)


def get_all_camper_in_camp(db: Session):
    rows = db.query(CamperInCamp).all()
    return rows


def create_new_camper_in_camp(db: Session, new_camper_in_camp: CamperInCampCreate):
    db_camper_in_camp = None
    try:
        db_camper_in_camp = CamperInCamp(**new_camper_in_camp.dict())
        db.add(db_camper_in_camp)
        db.commit()
        db.refresh(db_camper_in_camp)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_in_camp = None
        return db_camper_in_camp
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_in_camp


def update_camper_in_camp_by_id(
    db: Session,
    camp_id: int,
    camper_id: int,
    modify_camper_in_camp: CamperInCampModify,
):
    print("######################################################")
    print(type(modify_camper_in_camp))
    rows_updated = (
        db.query(CamperInCamp)
        .filter(
            and_(CamperInCamp.camp_id == camp_id, CamperInCamp.camper_id == camper_id)
        )
        .update(modify_camper_in_camp, synchronize_session="fetch")
    )
    print(rows_updated)
    db.commit()
    return rows_updated


def get_subscribe_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camper.id.label("camper_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
            CamperInCamp.payment_balance.label("camper_payment_balance"),
        )
        .join(Camp, CamperInCamp.camp_id == Camp.id)
        .join(Camper, CamperInCamp.camper_id == Camper.id)
        .join(Constant, CamperInCamp.status == Constant.id)
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.status == 36,
                Camp.active == True,
                Camp.start >= date.today(),
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_cancelled_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
            CamperInCamp.payment_balance.label("camper_payment_balance"),
        )
        .join(Camp, CamperInCamp.camp_id == Camp.id)
        .join(Constant, CamperInCamp.status == Constant.id)
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.status == 37,
                Camp.active == True,
                Camp.start >= date.today(),
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_all_cancelled_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
            CamperInCamp.payment_balance.label("camper_payment_balance"),
        )
        .join(Camp, CamperInCamp.camp_id == Camp.id)
        .join(Constant, CamperInCamp.status == Constant.id)
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.status == 37,
                Camp.active == True,
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_past_subscribe_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
            CamperInCamp.payment_balance.label("camper_payment_balance"),
        )
        .join(Camp, CamperInCamp.camp_id == Camp.id)
        .join(Constant, CamperInCamp.status == Constant.id)
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.status == 36,
                Camp.active == True,
                Camp.start < date.today(),
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_camper_in_camp_by_camper_camp(db: Session, camper_id: int, camp_id: int):
    camper_in_camp = (
        db.query(CamperInCamp)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.camp_id == camp_id,
                CamperInCamp.status == 36,
            )
        )
        .first()
    )
    if camper_in_camp:
        return camper_in_camp
    else:
        return False


def get_campers_for_module(db: Session, camp_id: int):
    campers = (
        db.query(
            Camper.id.label("camper_id"),
            Camper.name.label("camper_name"),
            Camper.lastname_father.label("camper_lastname_father"),
            Camper.lastname_mother.label("camper_lastname_mother"),
        )
        .join(CamperInCamp, CamperInCamp.camper_id == Camper.id)
        .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36))
        .all()
    )
    return db_mapping_rows_to_dict(campers)


def get_camps_name_amount_camper(db: Session, camper_id: int):
    data = []
    camps = get_subscribe_by_camper(db, camper_id)
    cancelled_camps = get_all_cancelled_by_camper(db, camper_id)

    for camp in camps:
        data.append(
            {
                "camp_id": getattr(camp, "camp_id"),
                "camp_name": getattr(camp, "camp_name"),
                "camper_payment_balance": getattr(camp, "camper_payment_balance"),
            }
        )

    for camp in cancelled_camps:
        if getattr(camp, "camper_payment_balance") > 0:
            data.append(
                {
                    "camp_id": getattr(camp, "camp_id"),
                    "camp_name": getattr(camp, "camp_name"),
                    "camper_payment_balance": getattr(camp, "camper_payment_balance"),
                }
            )
    return data


def get_campers_for_camp(db: Session, camp_id: int):
    campers = (
        db.query(
            CamperInCamp.id.label("camper_in_camp_id"),
            Camper.record_id.label("camper_record_id"),
            CamperRecord.id.label("record_id"),
            Camper.id.label("camper_id"),
            Camper.photo.label("camper_photo"),
            (
                Camper.name
                + " "
                + Camper.lastname_father
                + " "
                + Camper.lastname_mother
            ).label("camper_full_name"),
            CamperRecord.attend.label("camper_attend"),
            CamperRecord.attended.label("camper_attended"),
            CamperRecord.total.label("camper_total"),
            CamperInCamp.payment_balance.label("camper_total_balance"),
            Camper.birthday.label("camper_birthday"),
            (
                Parent.tutor_name
                + " "
                + Parent.tutor_lastname_father
                + " "
                + Parent.tutor_lastname_mother
            ).label("tutor_full_name"),
            User.email.label("tutor_email"),
            (
                Parent.contact_name
                + " "
                + Parent.contact_lastname_father
                + " "
                + Parent.contact_lastname_mother
            ).label("second_tutor_full_name"),
            Parent.contact_email.label("second_tutor_email"),
        )
        .join(Camper, CamperInCamp.camper_id == Camper.id)
        .join(Parent, Camper.parent_id == Parent.id)
        .join(CamperRecord, Camper.record_id == CamperRecord.id)
        .join(User, Parent.user_id == User.id)
        .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36))
        .all()
    )
    return db_mapping_rows_to_dict(campers)
