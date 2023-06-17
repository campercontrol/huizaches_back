from sqlalchemy.exc import SQLAlchemyError

from model.campers import CamperExtraAnswer
from model.camps import CampExtraQuestion

from crud.camps.camp_extra_question_crud import get_extra_question_by_camp
from schema.campers.camper_extra_answer_schema import (
    CamperExtraAnswerCreate,
    CamperExtraAnswerModify,
)
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_extra_answer(db):
    rows = db.query(CamperExtraAnswer).all()
    return rows


def get_extra_answer_by_uuid(db, extra_answer_id: int):
    return db.query(CamperExtraAnswer).filter_by(id=extra_answer_id).first()


def create_new_extra_answer(db, new_extra_answer: CamperExtraAnswerCreate):
    db_extra_answer = None
    try:
        db_extra_answer = CamperExtraAnswer(**new_extra_answer.dict())
        db.add(db_extra_answer)
        db.commit()
        db.refresh(db_extra_answer)
    except SQLAlchemyError as e:
        print("#=================================#")
        print(e)
        print("#=================================#")
        db_extra_answer = None
        return db_extra_answer
    except Exception as e:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_extra_answer


def update_extra_answer_by_id(
    db, extra_answer_id:int, modify_extra_answer: CamperExtraAnswerModify
):
    rows_updated = (
        db.query(CamperExtraAnswer)
        .filter_by(id=extra_answer_id)
        .update(modify_extra_answer, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def get_extra_answer_by_camper_camp(db, camper_id:int, camp_id:int):
    
    extra_answers = []
    extra_questions = get_extra_question_by_camp(db, camp_id)
    for extra_question in extra_questions:
        extra_answers.append(
        db.query(CamperExtraAnswer.answer, CampExtraQuestion.question)
        .join(CampExtraQuestion, CampExtraQuestion.id==CamperExtraAnswer.question_id)
        .join(CamperExtraAnswer, CamperExtraAnswer.camper_id)
        .filter(CampExtraQuestion.id == getattr(extra_question, "id"))
        .all()
        )
        
    return extra_answers