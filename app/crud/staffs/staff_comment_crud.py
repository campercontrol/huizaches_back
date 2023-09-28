from sqlalchemy.exc import SQLAlchemyError

from model.staffs import StaffComment
from schema.staffs.staff_comment_schema import (
    StaffCommentCreate,
    StaffCommentModify,
)
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case, and_


def get_all_staff_comment(db):
    rows = db.query(StaffComment).all()
    return rows


def get_staff_comment_by_id(db, staff_comment_id: int):
    return db.query(StaffComment).filter_by(id=staff_comment_id).first()


def create_new_staff_comment(db, new_staff_comment: StaffCommentCreate):
    db_staff_comment = None
    try:
        db_staff_comment = StaffComment(**new_staff_comment.dict())
        db.add(db_staff_comment)
        db.commit()
        db.refresh(db_staff_comment)
    except SQLAlchemyError as e:
        print("#=================================#")
        print(e)
        print("#=================================#")
        db_staff_comment = None
        return db_staff_comment
    except Exception as e:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_staff_comment


def update_staff_comment_by_id(
    db, staff_comment_id: int, modify_staff_comment: StaffCommentModify
):
    rows_updated = (
        db.query(StaffCommentModify)
        .filter_by(id=staff_comment_id)
        .update(modify_staff_comment, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_staff_comment_by_staff_for_staff(db, staff_id: int):
    rows = (
        db.query(StaffComment)
        .filter(
            and_(
                StaffComment.staff_id == staff_id,
                StaffComment.is_public == True,
                StaffComment.show_to == 38,
            )
        )
        .all()
    )
    return rows

def get_staff_comment_by_staff_for_admin(db, staff_id: int):
    rows = (
        db.query(StaffComment)
        .filter(
            and_(
                StaffComment.staff_id == staff_id,
                StaffComment.is_public == True
            )
        )
        .all()
    )
    return rows