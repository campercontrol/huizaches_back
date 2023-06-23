from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.catalogs import FoodRestriction
from schema.catalogs.food_restriction_schema import (
    FoodRestrictionCreate,
    FoodRestrictionModify,
)


def get_all_food_restriction(db: Session):
    rows = db.query(FoodRestriction).all()
    return rows


def get_all_food_restriction_id_name(db: Session):
    rows = db.query(FoodRestriction.id, FoodRestriction.name).all()
    return db_mapping_rows_to_dict(rows)


def get_food_restriction_by_uuid(db: Session, food_restriction_id: int):
    return (
        db.query(FoodRestriction)
        .filter_by(
            id=food_restriction_id,
        )
        .first()
    )


def create_new_food_restriction(
    db: Session, new_food_restriction: FoodRestrictionCreate
):
    db_food_restriction = None
    try:
        db_food_restriction = FoodRestriction(
            id=new_food_restriction.id,
            name=new_food_restriction.name,
            assigned_id=new_food_restriction.assigned_id,
            order=new_food_restriction.order,
            created_at=new_food_restriction.created_at,
        )
        db.add(db_food_restriction)
        db.commit()
        db.refresh(db_food_restriction)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_food_restriction = None
        return db_food_restriction
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_food_restriction


def update_food_restriction_by_id(
    db: Session,
    food_restriction_id: int,
    modify_food_restriction: FoodRestrictionModify,
):
    rows_updated = (
        db.query(FoodRestriction)
        .filter_by(id=food_restriction_id)
        .update(modify_food_restriction, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def delete_food_restriction(db: Session, food_restriction_id:int):
    food_restriction = db.query(FoodRestriction).filter(FoodRestriction.id==food_restriction_id).first()
    db.delete(food_restriction)
    db.commit()
    return {"status" : True}