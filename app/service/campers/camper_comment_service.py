from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.campers.camper_comment_crud import (
    get_all_camper_comment,
    get_camper_comment_by_id,
    create_new_camper_comment,
    update_camper_comment_by_id,
    get_camper_comment_by_camper_for_parent
)
from schema.campers.camper_comment_schema import (
    CamperCommentCreate,
    CamperCommentModify,
)
from utils.db import SessionLocal

camper_comment_router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@camper_comment_router.get("/camper_comment/", tags=["CamperComment"])
def get_camper_comment(db: Session = Depends(get_db)):
    list_camper_comment = get_all_camper_comment(db)
    return {"data": list_camper_comment}


@camper_comment_router.get(
    "/camper_comment/{camper_comment_id}", tags=["CamperComment"]
)
def get_camper_comment_by_uid(
    camper_comment_id: str, db: Session = Depends(get_db)
):
    list_camper_comment = get_camper_comment_by_id(db, camper_comment_id)
    return {"data": list_camper_comment}


@camper_comment_router.post("/camper_comment/", tags=["CamperComment"])
def create_camper_comment(
    new_camper_comment: CamperCommentCreate, db: Session = Depends(get_db)
):
    response = create_new_camper_comment(db, new_camper_comment)
    if response['status'] == 3:
        raise HTTPException(status_code=500, detail= response)
    return {"detail": response}


@camper_comment_router.patch(
    "/camper_comment/{camper_comment_id}", tags=["CamperComment"]
)
def update_camper_comment(
    camper_comment_id: str,
    modify_camper_comment: CamperCommentModify,
    db: Session = Depends(get_db),
):
    update_data = modify_camper_comment.dict(exclude_unset=True)
    print(update_data)
    camper_comment_upcdate_result = update_camper_comment_by_id(
        db, camper_comment_id, update_data
    )

    if camper_comment_upcdate_result != 0:
        exist_camper_comment = get_camper_comment_by_id(db, camper_comment_id)
        return {
            "mensaje": "Actualizado Correctamente",
            "data": exist_camper_comment,
        }
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@camper_comment_router.get(
    "/camper_comment_for_parent/{camper_id}", tags=["CamperComment"]
)
def get_camper_comment_for_parent(
    camper_id: int, db: Session = Depends(get_db)
):
    list_camper_comment = get_camper_comment_by_camper_for_parent(db, camper_id)
    return {"data": list_camper_comment}