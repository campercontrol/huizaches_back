from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.campers.school_crud import (
    get_all_school,
    get_school_by_uuid,
    create_new_school,
    get_active_school,
    delete_school,
    school_dashboard,
    update_school_controller,
    get_upcoming_school_camps,
    get_past_school_camps
)    

from schema.campers.school_schema import(
    SchoolCreate,
    SchoolModify,
    UpdateSchool

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


@school_routes.get("/school/{school_id}/upcoming_camps", tags=["School"])
def upcoming_school_camps(school_id:str, db: Session = Depends(get_db)):
    upcoming_camps = get_upcoming_school_camps(db, school_id)
    return {"data": upcoming_camps}

@school_routes.get("/school/{school_id}/past_camps", tags=["School"])
def past_school_camps(school_id:str, db: Session = Depends(get_db)):
    past_school = get_past_school_camps(db, school_id)
    return {"data": past_school}

@school_routes.post("/school/", tags=["Campers"])
def create_school(new_school:SchoolCreate, db: Session =Depends(get_db)):
    result = create_new_school(db, new_school)
    
    if result == 1:
        return {"detail": {"status": 1, "msg": "La escuela se ha creado correctamente"}}
    if result == 2:
        return {"detail": {"status": 2, "msg": "Ya existe una cuenta con ese email"}}
    if result == 3:
        raise HTTPException(status_code=500, detail={"status": 3, "msg": "Ocurrio un error al crear la escuela"})

@school_routes.patch("/school/{school_id}", tags=["Campers"])
def update_school(school_id:str,modify_school:UpdateSchool,db: Session = Depends(get_db)):

    result = update_school_controller(db,school_id, modify_school)

    if result == 1:
        return {"detail": {"status": 1, "msg": "La escuela se ha actualizado correctamente"}}
    if result == 3:
        raise HTTPException(status_code=500, detail={"status": 3, "msg": "Ocurrió un eror al actualizar la escuela"})

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