from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.trophies.trophy_crud import (
    get_all_trophy,
    get_trophy_by_id,
    update_trophy_by_id,
    create_new_trophy,
    delete_trophy
)
from schema.trophies.trophy_schema import(
    TrophyCreate,
    TrophyModify
)
from utils.db import SessionLocal

trophy_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@trophy_routes.get("/trophy/", tags=["Trophies"])
def get_trophy(db: Session = Depends(get_db)):
    list_trophy = get_all_trophy(db)
    return {"data": list_trophy}

@trophy_routes.get("/trophy/{trophy_id}", tags=["Trophies"])
def get_trophy_by__id(trophy_id:str,db: Session = Depends(get_db)):
    trophy = get_trophy_by_id(db,trophy_id)
    return {"data": trophy}

@trophy_routes.post("/trophy/", tags=["Trophies"])
def create_trophy(new_trophy:TrophyCreate,db: Session = Depends(get_db)):
    trophy = create_new_trophy(db, new_trophy)
    return {"data": trophy}

@trophy_routes.patch("/trophy/{trophy_id}", tags=["Trophies"])
def update_trophy(trophy_id:str,modify_trophy:TrophyModify,db: Session = Depends(get_db)):

    update_data = modify_trophy.dict(exclude_unset=True)
    print(update_data)
    trophy_update_result = update_trophy_by_id(db,trophy_id,update_data)

    if trophy_update_result != 0:
        exist_trophy = get_trophy_by_id(db, trophy_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_trophy}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@trophy_routes.delete("/delete/trophy/{trophy_id}", tags=["Trophies"])
def delete_trophy_by_id(trophy_id:int, db: Session = Depends(get_db)):
    status = delete_trophy(db, trophy_id)
    return{"status": status}

