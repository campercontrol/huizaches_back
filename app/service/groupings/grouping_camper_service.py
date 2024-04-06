from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.groupings.grouping_camper_crud import (
    get_all_grouping_campers,
    get_grouping_camper_by_id,
    create_new_grouping_camper,
    update_grouping_camper,
    assign_grouping_camp_to_campers,
    get_available_campers_to_add_in_grouping
)
from schema.groupings.grouping_camper_schema import GroupingCamperCreate, GroupingCamperUpdate, GroupingCamperResponse, GroupingAvailableCampers
from utils.db import SessionLocal

grouping_camper_router = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@grouping_camper_router.get("/grouping_campers/", response_model=list[GroupingCamperResponse], tags=["GroupingCamper"])
def list_grouping_campers(db: Session = Depends(get_db)):
    return get_all_grouping_campers(db)

@grouping_camper_router.get("/grouping_campers/{grouping_camper_id}", response_model=GroupingCamperResponse, tags=["GroupingCamper"])
def get_grouping_camper(grouping_camper_id: int, db: Session = Depends(get_db)):
    db_grouping_camper = get_grouping_camper_by_id(db, grouping_camper_id)
    if db_grouping_camper is None:
        raise HTTPException(status_code=404, detail="GroupingCamper not found")
    return db_grouping_camper

@grouping_camper_router.get("/groupings/{grouping_camp_id}/available_campers", tags=["GroupingCamper"])
def get_available_campers_to_add_in_grouping(grouping_camp_id: int, db: Session = Depends(get_db)):
    db_available_campers_to_add = get_available_campers_to_add_in_grouping(grouping_camp_id, db)
    if len(db_available_campers_to_add) == 0:
      raise HTTPException(status_code=404, detail="Grouping_camp not found")  
    return db_available_campers_to_add


@grouping_camper_router.post("/grouping_campers/", tags=["GroupingCamper"])
def add_camper_to_grouping(grouping_camper: GroupingCamperCreate, db: Session = Depends(get_db)):
    return create_new_grouping_camper(db, grouping_camper)

# @grouping_camper_router.post("/grouping_campers/assign/", response_model=GroupingCamperResponse, tags=["GroupingCamper"])
# def create_grouping_camper(campers_id: list[int], grouping_camp_id: int, db: Session = Depends(get_db)):
#     return assign_grouping_camp_to_campers(db, campers_id, grouping_camp_id)

@grouping_camper_router.put("/grouping_campers/{grouping_camper_id}", response_model=GroupingCamperResponse, tags=["GroupingCamper"])
def update_grouping_camper_endpoint(
    grouping_camper_id: int, grouping_camper: GroupingCamperUpdate, db: Session = Depends(get_db)
):
    return update_grouping_camper(db, grouping_camper_id, grouping_camper)
