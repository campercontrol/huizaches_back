from sqlalchemy.exc import SQLAlchemyError

from model.campers import CamperComment
from schema.campers.camper_comment_schema import (
    CamperCommentCreate,
    CamperCommentModify,
)
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case, and_


def get_all_camper_comment(db):
    rows = db.query(CamperComment).all()
    return rows


def get_camper_comment_by_id(db, camper_comment_id: int):
    return db.query(CamperComment).filter_by(id=camper_comment_id).first()


def create_new_camper_comment(db, new_camper_comment: CamperCommentCreate):
    try:
        db_camper_comment = CamperComment(**new_camper_comment.dict())
        db.add(db_camper_comment)
        db.commit()
        db.refresh(db_camper_comment)
    except SQLAlchemyError as alchemyError:
        db.rollback()
        print("#=================================#")
        print(alchemyError)
        print("#=================================#")
        return {"status": 3, "msg": "An error ocurred while saving"} 
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
        return {"status": 3, "msg": "An error ocurred while saving"}
    return {"status": 1, "msg": "Camper comment saved succesfully"}


def update_camper_comment_by_id(
    db, camper_comment_id: int, modify_camper_comment: CamperCommentModify
):
    rows_updated = (
        db.query(CamperCommentModify)
        .filter_by(id=camper_comment_id)
        .update(modify_camper_comment, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_camper_comment_by_camper_for_parent(db, camper_id: int):
    rows = (
        db.query(CamperComment)
        .filter(
            and_(
                CamperComment.camper_id == camper_id,
                CamperComment.is_public == True,
                CamperComment.show_to == 1,
            )
        )
        .all()
    )
    return rows


def get_camper_comment_by_camper_for_admin(db, camper_id: int):
    rows = (
        db.query(CamperComment)
        .filter(
            and_(
                CamperComment.camper_id == camper_id,
                CamperComment.is_public == True,
                CamperComment.show_to == 2,
            )
        )
        .all()
    )
    return rows
