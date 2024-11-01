from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.groupings.grouping_crud import (
    get_all_groupings,
    get_grouping_by_id,
    create_new_grouping,
    update_grouping,
    delete_grouping,
    delete_grouping_camper
)
from schema.groupings.grouping_schema import GroupingBase, GroupingCreate, GroupingUpdate, GroupingGet, GroupingResponse
from utils.db import SessionLocal

grouping_router = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@grouping_router.get("/groupings/", tags=["Grouping"])
def list_groupings(db: Session = Depends(get_db)):
    return get_all_groupings(db)


@grouping_router.get("/groupings/{grouping_id}", response_model=GroupingGet, tags=["Grouping"])
def read_grouping(grouping_id: int, db: Session = Depends(get_db)):
    db_grouping = get_grouping_by_id(db, grouping_id)
    if db_grouping is None:
        raise HTTPException(status_code=404, detail="Grouping not found")
    return db_grouping


@grouping_router.post("/groupings/", response_model=GroupingCreate, tags=["Grouping"])
def create_grouping(grouping: GroupingCreate, db: Session = Depends(get_db)):
    return create_new_grouping(db, grouping)


@grouping_router.patch("/groupings/{grouping_id}", tags=["Grouping"])
def update_grouping_endpoint(
    grouping_id: int, grouping: GroupingUpdate, db: Session = Depends(get_db)
):
    update_grouping_dict = grouping.dict(exclude_unset= True)
    grouping_update_result = update_grouping(db, grouping_id, update_grouping_dict)
    if grouping_update_result['status'] == 3:
        raise HTTPException(status_code=500, detail=grouping_update_result)
    return {"detail": grouping_update_result}



@grouping_router.delete("/groupings/{grouping_id}", tags=["Grouping"])
def delete_grouping_endpoint(grouping_id: int, db: Session = Depends(get_db)):
    if delete_grouping(db, grouping_id):
        return {"message": "Grouping deleted successfully"}
    raise HTTPException(status_code=404, detail="Grouping not found")


@grouping_router.delete("/grouping_camper/{grouping_camper_id}", tags=["Grouping"])
def remove_camper_from_grouping(grouping_camper_id: int, db: Session = Depends(get_db)):
    
    result = delete_grouping_camper(db, grouping_camper_id)
    if result == 1:
        return {"detail": {"msg": "Camper removed successfully from grouping.", "status": 1}}
    
    if result == 2:
        return {"detail": {"msg": "Grouping_camper_id does not exist.", "status": 2}}  
    
    if result == 3:
        return {"detail": {"msg": "An error ocurred while removing camper from grouping.", "status": 3}}
