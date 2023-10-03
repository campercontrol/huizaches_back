from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.trophies.trophy_season_crud import (
    get_all_trophy_season,
    get_trophy_season_by_id,
    update_trophy_season_by_id,
    create_new_trophy_season,
    delete_trophy_season
)
from schema.trophies.trophy_schema import(
    TrophySeasonCreate,
    TrophySeasonModify
)
from utils.db import SessionLocal

trophy_season_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@trophy_season_routes.get("/trophy_season/", tags=["Trophies"])
def get_trophy_season(db: Session = Depends(get_db)):
    list_trophy_season = get_all_trophy_season(db)
    return {"data": list_trophy_season}

@trophy_season_routes.get("/trophy_season/{trophy_season_id}", tags=["Trophies"])
def get_trophy_season_by__id(trophy_season_id:str,db: Session = Depends(get_db)):
    trophy_season = get_trophy_season_by_id(db,trophy_season_id)
    return {"data": trophy_season}

@trophy_season_routes.post("/trophy_season/", tags=["Trophies"])
def create_trophy_season(new_trophy_season:TrophySeasonCreate,db: Session = Depends(get_db)):
    trophy_season = create_new_trophy_season(db, new_trophy_season)
    return {"data": trophy_season}

@trophy_season_routes.patch("/trophy_season/{trophy_season_id}", tags=["Trophies"])
def update_trophy_season(trophy_season_id:str,modify_trophy_season:TrophySeasonModify,db: Session = Depends(get_db)):

    update_data = modify_trophy_season.dict(exclude_unset=True)
    print(update_data)
    trophy_season_update_result = update_trophy_season_by_id(db,trophy_season_id,update_data)

    if trophy_season_update_result != 0:
        exist_trophy_season = get_trophy_season_by_id(db, trophy_season_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_trophy_season}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@trophy_season_routes.delete("/delete/trophy_season/{trophy_season_id}", tags=["Trophies"])
def delete_trophy_season_by_id(trophy_season_id:int, db: Session = Depends(get_db)):
    status = delete_trophy_season(db, trophy_season_id)
    return{"status": status}

