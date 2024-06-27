from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.groupings.grouping_type_crud import (
    get_all_grouping_types,
    get_grouping_type_by_id,
    create_new_grouping_type,
    update_grouping_type,
    delete_grouping_type
)
from schema.groupings.grouping_type_schema import GroupingTypeBase, GroupingTypeCreate, GroupingTypeUpdate, GroupingTypeResponse
from utils.db import SessionLocal

grouping_type_router = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@grouping_type_router.get("/grouping_types/", response_model=list[GroupingTypeResponse], tags=["GroupingType"])
def list_grouping_types(db: Session = Depends(get_db)):
    return get_all_grouping_types(db)

@grouping_type_router.get("/grouping_types/{grouping_type_id}", response_model=GroupingTypeResponse, tags=["GroupingType"])
def read_grouping_type(grouping_type_id: int, db: Session = Depends(get_db)):
    db_grouping_type = get_grouping_type_by_id(db, grouping_type_id)
    if db_grouping_type is None:
        raise HTTPException(status_code=404, detail="GroupingType not found")
    return db_grouping_type

@grouping_type_router.post("/grouping_types/", response_model=GroupingTypeResponse, tags=["GroupingType"])
def create_grouping_type(grouping_type: GroupingTypeCreate, db: Session = Depends(get_db)):
    return create_new_grouping_type(db, grouping_type)

@grouping_type_router.patch("/grouping_types/{grouping_type_id}", tags=["GroupingType"])
def update_grouping_type_endpoint(
    grouping_type_id: int, grouping_type: GroupingTypeUpdate, db: Session = Depends(get_db)
):
    update_grouping_type_result = update_grouping_type(db, grouping_type_id, grouping_type)
    if update_grouping_type_result['status'] == 3:
        raise HTTPException(status_code=500, detail=update_grouping_type_result)
    return {"detail": update_grouping_type_result}

@grouping_type_router.delete("/grouping_types/{grouping_type_id}", tags=["GroupingType"])
def delete_grouping_type_endpoint(grouping_type_id: int, db: Session = Depends(get_db)):
    if delete_grouping_type(db, grouping_type_id):
        return {"message": "GroupingType deleted successfully"}
    raise HTTPException(status_code=404, detail="GroupingType not found")
