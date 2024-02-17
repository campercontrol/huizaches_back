from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.trophies.trophy_staff_crud import (
    get_all_trophy_staff,
    get_trophy_staff_by_id,
    update_trophy_staff_by_id,
    create_new_trophy_staff,
    delete_trophy_staff
)
from schema.trophies.trophy_schema import(
    TrophyStaffCreate,
    TrophyStaffModify
)
from utils.db import SessionLocal

trophy_staff_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@trophy_staff_routes.get("/trophy_staff/", tags=["Trophies"])
def get_trophy_staff(db: Session = Depends(get_db)):
    list_trophy_staff = get_all_trophy_staff(db)
    return {"data": list_trophy_staff}

@trophy_staff_routes.get("/trophy_staff/{trophy_staff_id}", tags=["Trophies"])
def get_trophy_staff_by__id(trophy_staff_id:str,db: Session = Depends(get_db)):
    trophy_staff = get_trophy_staff_by_id(db,trophy_staff_id)
    return {"data": trophy_staff}

@trophy_staff_routes.post("/trophy_staff/", tags=["Trophies"])
def create_trophy_staff(new_trophy_staff:TrophyStaffCreate,db: Session = Depends(get_db)):
    trophy_staff = create_new_trophy_staff(db, new_trophy_staff)
    return {"data": trophy_staff}

@trophy_staff_routes.patch("/trophy_staff/{trophy_staff_id}", tags=["Trophies"])
def update_trophy_staff(trophy_staff_id:str,modify_trophy_staff:TrophyStaffModify,db: Session = Depends(get_db)):

    update_data = modify_trophy_staff.dict(exclude_unset=True)
    print(update_data)
    trophy_staff_update_result = update_trophy_staff_by_id(db,trophy_staff_id,update_data)

    if trophy_staff_update_result != 0:
        exist_trophy_staff = get_trophy_staff_by_id(db, trophy_staff_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_trophy_staff}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@trophy_staff_routes.delete("/delete/trophy_staff/{trophy_staff_id}", tags=["Trophies"])
def delete_trophy_staff_by_id(trophy_staff_id:int, db: Session = Depends(get_db)):
    status = delete_trophy_staff(db, trophy_staff_id)
    return{"status": status}

