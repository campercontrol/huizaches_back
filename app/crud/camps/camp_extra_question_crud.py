from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import CampExtraQuestion
from model.camps import Camp

from schema.camps.camp_extra_question_schema import (
    CampExtraQuestionCreate,
    CampExtraQuestionModify,
)


def get_all_extra_question(db):
    rows = db.query(CampExtraQuestion).all()
    return rows


def get_extra_question_by_id(db, extra_question_id: int):
    return (
        db.query(CampExtraQuestion)
        .filter_by(
            id=extra_question_id,
        )
        .first()
    )


def create_new_extra_question(db, new_extra_question: CampExtraQuestionCreate):
    db_extra_question = None
    try:
        db_extra_question = CampExtraQuestion(**new_extra_question.dict())
        db.add(db_extra_question)
        db.commit()
        db.refresh(db_extra_question)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_extra_question = None
        return db_extra_question
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_extra_question


def update_extra_question_by_id(db, extra_question_id: int, modify_extra_question: CampExtraQuestionModify):
    rows_updated = (
        db.query(CampExtraQuestion)
        .filter_by(id=extra_question_id)
        .update(modify_extra_question, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_extra_question_by_camp(db, camp_id: int):
    rows = (
        db.query(CampExtraQuestion)
        .select_from(CampExtraQuestion)
        .filter(CampExtraQuestion.camp_id == camp_id)
        .all()
    )
    return rows

def delete_extra_question(db: Session, extra_question_id:int):
    extra_question = db.query(CampExtraQuestion).filter(CampExtraQuestion.id==extra_question_id).first()
    db.delete(extra_question)
    db.commit()
    return {"status" : True}
