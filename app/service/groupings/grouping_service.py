from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.groupings.grouping_crud import (
    get_all_groupings,
    get_grouping_by_id,
    create_new_grouping,
    update_grouping,
    delete_grouping
)
from schema.groupings.grouping_schema import GroupingCreate, GroupingUpdate
from utils.db import SessionLocal

grouping_router = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@grouping_router.get("/groupings/", response_model=list[GroupingCreate], tags=["Grouping"])
def list_groupings(db: Session = Depends(get_db)):
    return get_all_groupings(db)


@grouping_router.get("/groupings/{grouping_id}", response_model=GroupingCreate, tags=["Grouping"])
def read_grouping(grouping_id: int, db: Session = Depends(get_db)):
    db_grouping = get_grouping_by_id(db, grouping_id)
    if db_grouping is None:
        raise HTTPException(status_code=404, detail="Grouping not found")
    return db_grouping


@grouping_router.post("/groupings/", response_model=GroupingCreate, tags=["Grouping"])
def create_grouping(grouping: GroupingCreate, db: Session = Depends(get_db)):
    return create_new_grouping(db, grouping)


@grouping_router.put("/groupings/{grouping_id}", response_model=GroupingUpdate, tags=["Grouping"])
def update_grouping_endpoint(
    grouping_id: int, grouping: GroupingUpdate, db: Session = Depends(get_db)
):
    return update_grouping(db, grouping_id, grouping)


@grouping_router.delete("/groupings/{grouping_id}", tags=["Grouping"])
def delete_grouping_endpoint(grouping_id: int, db: Session = Depends(get_db)):
    if delete_grouping(db, grouping_id):
        return {"message": "Grouping deleted successfully"}
    raise HTTPException(status_code=404, detail="Grouping not found")
