from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from model.staffs import StaffFoodRestriction
from schema.staff_catalogs.staff_food_restriction_schema import (
    StaffFoodRestrictionCreate,
    StaffFoodRestrictionModify,
)


def get_all_staff_food_restriction(db: Session):
    rows = db.query(StaffFoodRestriction).all()
    return rows


def get_all_staff_food_restriction_id_name(db: Session):
    rows = db.query(StaffFoodRestriction.id, StaffFoodRestriction.name).all()
    return db_mapping_rows_to_dict(rows)


def get_staff_food_restriction_by_uuid(db: Session, staff_food_restriction_id: int):
    return (
        db.query(StaffFoodRestriction)
        .filter_by(
            id=staff_food_restriction_id,
        )
        .first()
    )


def get_staff_food_restriction_by_food_r(db: Session, food_restriction_id: int):
    return (
        db.query(StaffFoodRestriction)
        .filter_by(
            food_restriction_id=food_restriction_id,
        )
        .first()
    )


def create_new_staff_food_restriction(
    db: Session, new_staff_food_restriction: StaffFoodRestrictionCreate
):
    db_staff_food_restriction = None
    try:
        db_staff_food_restriction = StaffFoodRestriction(
            **new_staff_food_restriction.dict()
        )
        db.add(db_staff_food_restriction)
        db.commit()
        db.refresh(db_staff_food_restriction)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_staff_food_restriction = None
        return db_staff_food_restriction
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_staff_food_restriction


def update_staff_food_restriction_by_id(
    db: Session,
    staff_food_restriction_id: int,
    staff_id: int,
    modify_staff_food_restriction: StaffFoodRestrictionModify,
):
    print("######################################################")
    print(type(modify_staff_food_restriction))
    rows_updated = (
        db.query(StaffFoodRestriction)
        .filter_by(food_restriction_id=staff_food_restriction_id, staff_id=staff_id)
        .update(modify_staff_food_restriction, synchronize_session="fetch")
    )
    print(rows_updated)
    db.commit()
    return rows_updated
