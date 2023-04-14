from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import case

from utils.db import db_mapping_rows_to_dict

from model.campers import Camper
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


def get_all_camper(db: Session) -> any:
    rows = db.query(Camper).all()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(rows)
    return rows


def get_camper_by_uuid(db: Session, camper_id: int) -> any:
    return db.query(Camper).filter_by(id=camper_id).first()


def create_new_camper(db: Session, new_camper: CamperCreate) -> any:
    db_camper = None
    try:
        db_camper = Camper(**new_camper.dict())
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
        .join(Vaccine, CamperLicensedMedicine.licensed_medicine_id == Vaccine.id)
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
    return db.query(Camper).filter_by(parent_id=parent_id).all()

