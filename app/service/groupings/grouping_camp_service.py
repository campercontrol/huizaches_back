from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.groupings.grouping_camp_crud import (
    get_all_grouping_camps,
    get_grouping_camp_by_id,
    get_camp_groupings_by_camp_id,
    create_new_grouping_camp,
    update_grouping_camp,
)
from schema.groupings.grouping_camp_schema import GroupingCampCreate, GroupingCampUpdate, GroupingCampResponse
from utils.db import SessionLocal

grouping_camp_router = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@grouping_camp_router.get("/grouping_camps/", response_model=list[GroupingCampResponse], tags=["GroupingCamp"])
def list_grouping_camps(db: Session = Depends(get_db)):
    return get_all_grouping_camps(db)

@grouping_camp_router.get("/grouping_camps/{grouping_camp_id}", response_model=GroupingCampResponse, tags=["GroupingCamp"])
def read_grouping_camp(grouping_camp_id: int, db: Session = Depends(get_db)):
    db_grouping_camp = get_grouping_camp_by_id(db, grouping_camp_id)
    if db_grouping_camp is None:
        raise HTTPException(status_code=404, detail="GroupingCamp not found")
    return db_grouping_camp

@grouping_camp_router.get("/camps/{camp_id}/groupings", tags=["GroupingCamp"])
def get_groupings_by_camp(camp_id: int, db: Session = Depends(get_db)):
    db_camp_groupings = get_camp_groupings_by_camp_id(db, camp_id)
    if len(db_camp_groupings) == 0:
        raise HTTPException(status_code=404, detail="Camp not found")
    return {"data": db_camp_groupings }

@grouping_camp_router.post("/grouping_camps/", response_model=GroupingCampResponse, tags=["GroupingCamp"])
def create_grouping_camp(grouping_camp: GroupingCampCreate, db: Session = Depends(get_db)):
    return create_new_grouping_camp(db, grouping_camp)

@grouping_camp_router.put("/grouping_camps/{grouping_camp_id}", response_model=GroupingCampResponse, tags=["GroupingCamp"])
def update_grouping_camp_endpoint(
    grouping_camp_id: int, grouping_camp: GroupingCampUpdate, db: Session = Depends(get_db)
):
    return update_grouping_camp(db, grouping_camp_id, grouping_camp)
