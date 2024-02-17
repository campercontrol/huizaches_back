from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.camps.camp_extra_question_crud import (
    get_all_extra_question,
    get_extra_question_by_id,
    get_extra_question_by_camp,
    create_new_extra_question,
    update_extra_question_by_id,
    delete_extra_question
)

from schema.camps.camp_extra_question_schema import (
    CampExtraQuestionCreate,
    CampExtraQuestionModify,
)
from utils.db import SessionLocal

extra_question_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@extra_question_routes.get("/camp_extra_question/", tags=["CampsExtraQuestion"])
def get_camp_extra_question(db: Session = Depends(get_db)):
    list_camp_extra_question = get_all_extra_question(db)
    return {"data": list_camp_extra_question}


@extra_question_routes.get("/camp_extra_question/{camp_extra_question_id}", tags=["CampsExtraQuestion"])
def get_camp_extra_question_by_id(
    camp_extra_question_id: str, db: Session = Depends(get_db)
):
    list_camp_extra_question = get_extra_question_by_id(db, camp_extra_question_id)
    return {"data": list_camp_extra_question}


@extra_question_routes.post("/camp_extra_question/", tags=["CampsExtraQuestion"])
def create_camp_extra_question(
    new_camp_extra_question: CampExtraQuestionCreate, db: Session = Depends(get_db)
):
    list_camp_extra_question = create_new_extra_question(db, new_camp_extra_question)
    return {"data": list_camp_extra_question}


@extra_question_routes.patch(
    "/camp_extra_question/{camp_extra_question_id}", tags=["CampsExtraQuestion"]
)
def update_camp_extra_question(
    camp_extra_question_id: int,
    modify_camp_extra_question: CampExtraQuestionModify,
    db: Session = Depends(get_db),
):
    update_data = modify_camp_extra_question.dict(exclude_unset=True)
    print(update_data)
    camp_extra_question_update_result = update_extra_question_by_id(
        db, camp_extra_question_id, update_data
    )

    if camp_extra_question_update_result != 0:
        exist_camp_extra_question = get_extra_question_by_id(
            db, camp_extra_question_id
        )
        return {"mensaje": "Actualizado Correctamente", "data": exist_camp_extra_question}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@extra_question_routes.get("/extra_question_by_camp/{camp_id}", tags=["CampsExtraQuestion"])
def extra_question_bycamp(camp_id, db: Session = Depends(get_db)):
    list_extra_questions = get_extra_question_by_camp(db, camp_id)
    return{"data": list_extra_questions}

@extra_question_routes.delete("/delete/camp_extra_question/{camp_extra_question_id}", tags=["CampsExtraQuestion"])
def delete_camp_extra_question_by_id(camp_extra_question_id:int, db: Session = Depends(get_db)):
    status = delete_extra_question(db, camp_extra_question_id)
    return{"status": status}


