from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.campers import CamperFoodRestriction
from model.catalogs import FoodRestriction
from schema.campers_catalogs.camper_food_restriction_schema import (
    CamperFoodRestrictionCreate,
    CamperFoodRestrictionModify,
)



def get_all_camper_food_restriction(db: Session):
    rows = db.query(CamperFoodRestriction).all()
    return rows


def get_all_camper_food_restriction_id_name(db: Session):
    rows = db.query(CamperFoodRestriction.id, CamperFoodRestriction.name).all()
    return db_mapping_rows_to_dict(rows)


def get_camper_food_restriction_by_uuid(db: Session, camper_food_restriction_id: int):
    return (
        db.query(CamperFoodRestriction)
        .filter_by(
            id=camper_food_restriction_id,
        )
        .first()
    )
def get_camper_food_restriction(db, camper_id):
    rows = (
        db.query(
            FoodRestriction.id,
            FoodRestriction.name,
            CamperFoodRestriction.is_active,
        ).select_from(CamperFoodRestriction)
        .join(FoodRestriction, CamperFoodRestriction.food_restriction_id == FoodRestriction.id)
        .filter(CamperFoodRestriction.camper_id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)

def create_new_camper_food_restriction(
    db: Session, new_camper_food_restriction: CamperFoodRestrictionCreate
):
    db_camper_food_restriction = None
    try:
        db_camper_food_restriction = CamperFoodRestriction(
            id=new_camper_food_restriction.id,
            camper_id=new_camper_food_restriction.camper_id,
            food_restriction_id=new_camper_food_restriction.food_restriction_id,
            is_active=new_camper_food_restriction.is_active,
        )
        db.add(db_camper_food_restriction)
        db.commit()
        db.refresh(db_camper_food_restriction)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_food_restriction = None
        return db_camper_food_restriction
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_food_restriction


def update_camper_food_restriction_by_ids(
    db: Session,
    camper_food_restriction_id: int,
    camper_id:int,
    modify_camper_food_restriction: CamperFoodRestrictionModify,
):
    rows_updated = (
        db.query(CamperFoodRestriction)
        .filter_by(food_restriction_id=camper_food_restriction_id, camper_id=camper_id)
        .update(modify_camper_food_restriction, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated
