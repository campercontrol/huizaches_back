from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import case, or_
from datetime import date, datetime

from utils.db import db_mapping_rows_to_dict

from model.campers import Camper, School, CamperRecord, Parent
from model.user import User
from model.catalogs import (
    Vaccine,
    FoodRestriction,
    LicensedMedicine,
    PathologicalBackground,
    PathologicalBackgroundFamily,
)
from model.campers import (
    CamperVaccine,
    CamperLicensedMedicine,
    CamperFoodRestriction,
    CamperPathologicalBackground,
    CamperPathologicalBackgroundFamily,
)
from schema.campers.camper_schema import CamperCreate, CamperModify, CamperComplete
from schema.campers.camper_record_schema import CamperRecordCreate
from crud.campers.camper_record_crud import create_new_camper_record


def get_all_camper(db: Session) -> any:
    rows = db.query(Camper).all()
    return rows


def get_camper_by_uuid(db: Session, camper_id: int) -> any:
    return db.query(Camper).filter_by(id=camper_id).first()


def create_new_camper(db: Session, new_camper: CamperCreate) -> any:
    db_camper = None
    try:
        new_camper_record = CamperRecordCreate(attend=0, attended=0, total=0)
        camper_record = create_new_camper_record(db, new_camper_record)
        new_camper = new_camper.dict()
        new_camper["record_id"] = camper_record.id
        db_camper = Camper(**new_camper)
        db.add(db_camper)
        db.commit()        
        db.refresh(db_camper)
    except SQLAlchemyError as e:
        print("#=================================#")
        print(e)
        print("#=================================#")
        db_camper = None
        return db_camper
    except Exception as e:
        print(f"No se pudo guardar en la base de datos: {e}")
    return db_camper

def update_camper_by_id(
    db: Session, camper_id: int, modify_camper: CamperModify
) -> any:
    print("#################################################")
    print(type(modify_camper))
    rows_updated = (
        db.query(Camper)
        .filter_by(id=camper_id)
        .update(modify_camper, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_vaccine_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(Vaccine.id, Vaccine.name, CamperVaccine.is_active)
        .join(Camper, CamperVaccine.camper_id == Camper.id)
        .join(Vaccine, CamperVaccine.vaccine_id == Vaccine.id)
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_licensed_medicine_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            LicensedMedicine.id, LicensedMedicine.name, CamperLicensedMedicine.is_active
        )
        .join(Camper, CamperLicensedMedicine.camper_id == Camper.id)
        .join(
            LicensedMedicine,
            CamperLicensedMedicine.licensed_medicine_id == LicensedMedicine.id,
        )
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_food_restriction_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            FoodRestriction.id, FoodRestriction.name, CamperFoodRestriction.is_active
        )
        .join(Camper, CamperFoodRestriction.camper_id == Camper.id)
        .join(
            FoodRestriction,
            CamperFoodRestriction.food_restriction_id == FoodRestriction.id,
        )
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_pathological_background_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            PathologicalBackground.id,
            PathologicalBackground.name,
            CamperPathologicalBackground.is_active,
        )
        .join(Camper, CamperPathologicalBackground.camper_id == Camper.id)
        .join(
            PathologicalBackground,
            CamperPathologicalBackground.pathological_background_id
            == PathologicalBackground.id,
        )
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_pathological_background_fm_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            PathologicalBackgroundFamily.id,
            PathologicalBackgroundFamily.name,
            CamperPathologicalBackgroundFamily.is_active,
        )
        .join(Camper, CamperPathologicalBackgroundFamily.camper_id == Camper.id)
        .join(
            PathologicalBackgroundFamily,
            CamperPathologicalBackgroundFamily.pathological_background_family_id
            == PathologicalBackgroundFamily.id,
        )
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_campers_from_parent(db: Session, parent_id: int):
    rows = (
        db.query(
            Camper.id,
            Camper.photo,
            (
                Camper.name
                + " "
                + Camper.lastname_father
                + " "
                + Camper.lastname_mother
            ).label("full_name"),
            School.name.label("school"),
        )
        .join(School, School.id == Camper.school_id)
        .filter(Camper.parent_id == parent_id)
        .all()
    )

    return db_mapping_rows_to_dict(rows)


def get_camper_band(db: Session, camper_id):
    camper = (
        db.query(
            (
                Camper.name
                + " "
                + Camper.lastname_father
                + " "
                + Camper.lastname_mother
            ).label("full_name"),
            School.name.label("school"),
            Camper.photo.label("photo"),
            Camper.birthday.label("birthday"),
            CamperRecord.attend.label("future_camps"),
            CamperRecord.attended.label("past_camps"),
        )
        .join(School, School.id == Camper.school_id)
        .join(CamperRecord, CamperRecord.id == Camper.record_id)
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(camper)


def delete_camper(db, camper_id: int):
    camper = db.query(Camper).filter(Camper.id == camper_id).first()
    db.delete(camper)
    db.commit()
    return {"status": True}


def search_camper_by_name_user(db: Session, search: str):
    campers = (
        db.query(
            Camper.id.label("camper_id"),
            Camper.name.label("camper_name"),
            Camper.lastname_father.label("camper_lastname_father"),
            Camper.lastname_mother.label("camper_lastname_mother"),
            School.name.label("school"),
            Camper.updated_at.label("updated"),
            Parent.id.label("tutor_id"),
            (
                Parent.tutor_name
                + " "
                + Parent.tutor_lastname_father
                + " "
                + Parent.tutor_lastname_mother
            ).label("tutor_fullname"),
            User.id.label("user_id"),
            User.email.label("tutor_email"),
        )
        .join(Parent, Parent.id == Camper.parent_id)
        .join(User, User.id == Parent.user_id)
        .join(School, School.id == Camper.school_id)
        .filter(
            or_(
                Camper.name.ilike(r"%{}%".format(search)),
                Camper.lastname_father.ilike(r"%{}%".format(search)),
                Camper.lastname_mother.ilike(r"%{}%".format(search)),
                School.name.ilike(r"%{}%".format(search)),
                Parent.tutor_name.ilike(r"%{}%".format(search)),
                Parent.tutor_lastname_father.ilike(r"%{}%".format(search)),
                Parent.tutor_lastname_mother.ilike(r"%{}%".format(search)),
                User.email.ilike(r"%{}%".format(search)),
            )
        )
        .all()
    )
    if campers:
        return db_mapping_rows_to_dict(campers)
    else:
        return "Data not found"


def get_all_camper_admin(db: Session):
    campers = (
        db.query(
            Camper.id.label("camper_id"),
            Camper.name.label("camper_name"),
            Camper.lastname_father.label("camper_lastname_father"),
            Camper.lastname_mother.label("camper_lastname_mother"),
            School.name.label("school"),
            Camper.updated_at.label("updated"),
            Parent.id.label("tutor_id"),
            (
                Parent.tutor_name
                + " "
                + Parent.tutor_lastname_father
                + " "
                + Parent.tutor_lastname_mother
            ).label("tutor_fullname"),
            User.id.label("user_id"),
            User.email.label("tutor_email"),
        )
        .join(Parent, Parent.id == Camper.parent_id)
        .join(User, User.id == Parent.user_id)
        .join(School, School.id == Camper.school_id)
        .all()
    )
    if campers:
        return db_mapping_rows_to_dict(campers)
    else:
        return "Data not found"
