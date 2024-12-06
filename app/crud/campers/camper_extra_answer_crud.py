from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from model.campers import CamperExtraAnswer
from model.camps import CampExtraQuestion, Camp


from schema.campers.camper_extra_answer_schema import (
    CamperExtraAnswerCreate,
    CamperExtraAnswerModify,
    UpdateCamperExtraAnswer,
    CamperExtraAnswerListCreate,
)


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
    db, extra_answers: UpdateCamperExtraAnswer
):
    rows_updated = None
    try:
        for extra_answer in extra_answers:
            rows_updated = (
                db.query(CamperExtraAnswer)
                .filter_by(id=extra_answer.id)
                .update(extra_answer.dict(), synchronize_session="fetch")
            )
        db.commit()
    except Exception as ex:
        print(f"An error ocurred while saving extra_answer {ex}" )
        db.rollback()
    print(rows_updated)
    return rows_updated

def update_extra_answers(db, extra_answer):
    try:
        for extra_answer in extra_answer:
            rows_updated = (
                db.query(CamperExtraAnswer)
                .filter_by(id=extra_answer.id)
                .update(extra_answer.dict(), synchronize_session="fetch")
        )
        db.commit()
        return 1
    except Exception as ex:
        print(ex)
        db.rollback()
        return 3


def get_extra_answer_by_camper_camp(db, camper_id: int, camp_id: int):
    query = db.query(
        CampExtraQuestion.id.label("question_id"),
        CampExtraQuestion.question.label("question"),
        CampExtraQuestion.is_required.label("is_required"),
        CampExtraQuestion.camp_id,
        Camp.name.label("camp_name"),
        CamperExtraAnswer.answer.label("answer"),
        CamperExtraAnswer.id.label("camper_extra_answer_id"),
        CamperExtraAnswer.camper_id).join(CamperExtraAnswer, CampExtraQuestion.id == CamperExtraAnswer.question_id).join(Camp, Camp.id == CampExtraQuestion.camp_id).filter(and_(CampExtraQuestion.camp_id == camp_id, CamperExtraAnswer.camper_id == camper_id))
    
    data = db.execute(query)
    data = data.mappings().all()
    return data


def create_update_extra_answers(db, extra_answers: CamperExtraAnswerListCreate):
    for extra_answer in extra_answers.extra_answers:
        row = (
            db.query(CamperExtraAnswer)
            .join(
                CampExtraQuestion, CampExtraQuestion.id == CamperExtraAnswer.question_id
            )
            .filter(CamperExtraAnswer.question_id == getattr(extra_answer, "id"))
            .first()
        )

        if row:
            camper_schema = CamperExtraAnswerModify(
                id=getattr(row, "id"),
                answer=getattr(extra_answer, "answer"),
                camper_id=getattr(row, "camper_id"),
                question_id=getattr(row, "question_id"),
            )
            answer = update_extra_answer_by_id(
                db, getattr(row, "id"), camper_schema.dict()
            )
        else:
            camper_schema = CamperExtraAnswerCreate(
                answer=getattr(extra_answer, "answer"),
                camper_id=getattr(extra_answer, "camper_id"),
                question_id=getattr(extra_answer, "id"),
            )
            answer = create_new_extra_answer(db, camper_schema)

    return answer
