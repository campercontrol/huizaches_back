from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.staffs.staff_comment_crud import (
    get_all_staff_comment,
    get_staff_comment_by_id,
    create_new_staff_comment,
    update_staff_comment_by_id,
    get_staff_comment_by_staff_for_staff
)
from schema.staffs.staff_comment_schema import (
    StaffCommentCreate,
    StaffCommentModify,
)
from utils.db import SessionLocal

staff_comment_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@staff_comment_routes.get("/staff_comment/", tags=["CamperComment"])
def get_staff_comment(db: Session = Depends(get_db)):
    list_staff_comment = get_all_staff_comment(db)
    return {"data": list_staff_comment}


@staff_comment_routes.get(
    "/staff_comment/{staff_comment_id}", tags=["CamperComment"]
)
def get_staff_comment_by_uid(
    staff_comment_id: str, db: Session = Depends(get_db)
):
    list_staff_comment = get_staff_comment_by_id(db, staff_comment_id)
    return {"data": list_staff_comment}


@staff_comment_routes.post("/staff_comment/", tags=["CamperComment"])
def create_staff_comment(
    new_staff_comment: StaffCommentCreate, db: Session = Depends(get_db)
):
    list_staff_comment = create_new_staff_comment(db, new_staff_comment)
    return {"data": list_staff_comment}


@staff_comment_routes.patch(
    "/staff_comment/{staff_comment_id}", tags=["CamperComment"]
)
def update_staff_comment(
    staff_comment_id: str,
    modify_staff_comment: StaffCommentModify,
    db: Session = Depends(get_db),
):
    update_data = modify_staff_comment.dict(exclude_unset=True)
    print(update_data)
    staff_comment_upcdate_result = update_staff_comment_by_id(
        db, staff_comment_id, update_data
    )

    if staff_comment_upcdate_result != 0:
        exist_staff_comment = get_staff_comment_by_id(db, staff_comment_id)
        return {
            "mensaje": "Actualizado Correctamente",
            "data": exist_staff_comment,
        }
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@staff_comment_routes.get(
    "/staff_comment_for_staff/{staff_id}", tags=["CamperComment"]
)
def get_staff_comment_for_staff(
    staff_id: int, db: Session = Depends(get_db)
):
    list_staff_comment = get_staff_comment_by_staff_for_staff(db, staff_id)
    return {"data": list_staff_comment}