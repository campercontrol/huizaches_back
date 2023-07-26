from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.camps.season_crud import (
    get_all_season,
    get_season_by_id,
    update_season_by_id,
    create_new_season
)
from schema.camps.season_schema import(
    SeasonCreate,
    SeasonModify
)
from utils.db import SessionLocal

season_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@season_routes.get("/season/", tags=["Camps"])
def get_season(db: Session = Depends(get_db)):
    list_season = get_all_season(db)
    return {"data": list_season}

@season_routes.get("/season/{season_id}", tags=["Camps"])
def get_season_by__id(season_id:str,db: Session = Depends(get_db)):
    season = get_season_by_id(db,season_id)
    return {"data": season}

@season_routes.post("/season/", tags=["Camps"])
def create_season(new_season:SeasonCreate,db: Session = Depends(get_db)):
    season = create_new_season(db, new_season)
    return {"data": season}

@season_routes.patch("/season/{season_id}", tags=["Camps"])
def update_season(season_id:str,modify_season:SeasonModify,db: Session = Depends(get_db)):

    update_data = modify_season.dict(exclude_unset=True)
    print(update_data)
    season_update_result = update_season_by_id(db,season_id,update_data)

    if season_update_result != 0:
        exist_season = get_season_by_id(db, season_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_season}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

