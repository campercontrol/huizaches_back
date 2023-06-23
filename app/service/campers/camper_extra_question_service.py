from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.campers.camper_extra_answer_crud import (
    get_all_extra_answer,
    get_extra_answer_by_uuid,
    create_new_extra_answer,
    update_extra_answer_by_id,
    get_extra_answer_by_camper_camp
)
from schema.campers.camper_extra_answer_schema import (
    CamperExtraAnswerCreate,
    CamperExtraAnswerModify,
)
from utils.db import SessionLocal

extra_answer_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@extra_answer_routes.get("/camper_extra_answer/", tags=["Campers"])
def get_camper_extra_answer(db: Session = Depends(get_db)):
    list_camper_extra_answer = get_all_extra_answer(db)
    return {"data": list_camper_extra_answer}


@extra_answer_routes.get(
    "/camper_extra_answer/{camper_extra_answer_id}", tags=["Campers"]
)
def get_camper_extra_answer_by_id(
    camper_extra_answer_id: str, db: Session = Depends(get_db)
):
    list_camper_extra_answer = get_extra_answer_by_uuid(db, camper_extra_answer_id)
    return {"data": list_camper_extra_answer}


@extra_answer_routes.post("/camper_extra_answer/", tags=["Campers"])
def create_camper_extra_answer(
    new_camper_extra_answer: CamperExtraAnswerCreate, db: Session = Depends(get_db)
):
    list_camper_extra_answer = create_new_extra_answer(db, new_camper_extra_answer)
    return {"data": list_camper_extra_answer}


@extra_answer_routes.patch(
    "/camper_extra_answer/{camper_extra_answer_id}", tags=["Campers"]
)
def update_camper_extra_answer(
    camper_extra_answer_id: str,
    modify_camper_extra_answer: CamperExtraAnswerModify,
    db: Session = Depends(get_db),
):
    update_data = modify_camper_extra_answer.dict(exclude_unset=True)
    print(update_data)
    camper_extra_answer_upcdate_result = update_extra_answer_by_id(
        db, camper_extra_answer_id, update_data
    )

    if camper_extra_answer_upcdate_result != 0:
        exist_camper_extra_answer = get_extra_answer_by_uuid(db, camper_extra_answer_id)
        return {
            "mensaje": "Actualizado Correctamente",
            "data": exist_camper_extra_answer,
        }
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@extra_answer_routes.get("/extra_answers_camper/{camp_id}/{camper_id}")
def get_extra_answers_camper(camp_id:int, camper_id:int, db:Session=Depends(get_db)):
    extra_answers =  get_extra_answer_by_camper_camp(db, camper_id, camp_id)
    return {"data": extra_answers}