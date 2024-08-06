from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.campers.school_crud import (
    get_all_school,
    get_school_by_uuid,
    create_new_school,
    update_school_by_id,
    get_active_school,
    delete_school,
    school_dashboard
)    

from schema.campers.school_schema import(
    SchoolCreate,
    SchoolModify

)
from utils.db import SessionLocal

school_routes = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@school_routes.get("/school/", tags=["Campers"])
def get_school(db: Session = Depends(get_db)):
    list_school = get_all_school(db)
    return {"data": list_school}

@school_routes.get("/school/{school_id}", tags=["Campers"])
def get_school_by_id(school_id:str, db: Session = Depends(get_db)):
    list_school = get_school_by_uuid(db, school_id)
    return {"data": list_school}

@school_routes.post("/school/", tags=["Campers"])
def create_school(new_school:SchoolCreate, db: Session =Depends(get_db)):
    result = create_new_school(db, new_school)
    
    if result == 1:
        return {"detail": {"status": 1, "msg": "School created successfully"}}
    if result == 2:
        return {"detail": {"status": 2, "msg": "Email account already in use"}}
    if result == 3:
        raise HTTPException(status_code=500, detail={"status": 3, "msg": "An unknown error ocurred while saving"})

@school_routes.patch("/school/{school_id}", tags=["Campers"])
def update_school(school_id:str,modify_school:SchoolModify,db: Session = Depends(get_db)):

    update_data = modify_school.dict(exclude_unset=True)
    print(update_data)
    school_upcdate_result = update_school_by_id(db,school_id,update_data)

    if school_upcdate_result != 0:
        exist_school = get_school_by_uuid(db, school_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_school}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}
    
@school_routes.get("/active_school/", tags=["Campers"])
def get_all_active_school(db: Session = Depends(get_db)):
    list_school = get_active_school(db)
    return {"data": list_school}

@school_routes.delete("/delete_school/{school_id}", tags=["Campers"])
def delete_school_by_id(school_id:int, db: Session = Depends(get_db)):
    status = delete_school(db, school_id)
    return{"status": status}

@school_routes.get("/school_dashboard/{school_id}", tags=["School"])
def get_staff_dashboard(staff_id: int, db: Session = Depends(get_db)):
    school_dashboard_info = school_dashboard(db, staff_id)
    return {"data": school_dashboard_info}