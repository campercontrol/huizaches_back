from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.camps.staff_in_camp_crud import (
    get_all_staff_in_camp,
    create_new_staff_in_camp,
    volunteer_staff,
    unsubscribe_staff,
    accept_staff_in_camp,
    assign_role_staff
)
from schema.camps.staff_in_camp_schema import(
    StaffInCampCreate,
    StaffInCampModify
)
from utils.db import SessionLocal

staff_in_camp_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@staff_in_camp_routes.get("/staff_in_camp/", tags=["StaffInCamp"])
def get_staff_in_camp(db: Session = Depends(get_db)):
    list_staff_in_camp = get_all_staff_in_camp(db)
    return {"data": list_staff_in_camp}


@staff_in_camp_routes.post("/staff_in_camp/", tags=["StaffInCamp"])
def create_staff_in_camp(new_staff_in_camp:StaffInCampCreate,db: Session = Depends(get_db)):
    staff_in_camp = create_new_staff_in_camp(db, new_staff_in_camp)
    return {"data": staff_in_camp}

@staff_in_camp_routes.post("/staff_volunteer/", tags=["StaffInCamp"])
def create_staff_volunteer(new_staff_in_camp:StaffInCampCreate, db: Session = Depends(get_db)):
    result = volunteer_staff(db, new_staff_in_camp)
    
    if result == 1:
        return {"detail": {"status": 1, "msg": "Se suscribió correctamente al prospecto."}}
    if result == 3:
        raise HTTPException(status_code=500, detail={"status": 3, "msg": "Se suscribió correctamente al prospecto."})
    
    

@staff_in_camp_routes.delete("/staff_unsubscribe/{id_staff_in_camp}", tags=["StaffInCamp"])
def unsubscribe_staff_to_camp(id_staff_in_camp:int , db: Session = Depends(get_db)):
    result = unsubscribe_staff(db, id_staff_in_camp)
    
    if result == 1:
        return {"detail": {"status": 1, "msg": "Se removió  correctamente al staff"}}
    if result == 3:
        raise HTTPException(status_code=500, detail={"status": 3, "msg": "Ocurrió un error inesperado al remover al staff, intente nuevamente más tarde"})
    

@staff_in_camp_routes.post("/accept/staff/camp/{camp_id}", tags=["StaffInCamp"])
def accept_staff_camp(staffs_id:list[int], camp_id:int, db: Session = Depends(get_db)):
    result = accept_staff_in_camp(db, camp_id, staffs_id)
    if result == 1:
        return {"detail": {"status": 1, "msg": "Se aceptó correctamente al staff"}}
    if result == 3:
        raise HTTPException(status_code=500, detail= {"status": 3, "msg": "Ocurrió un error al aceptar al staff, intente nuevamente mas tarde"}) 

@staff_in_camp_routes.post("/update/staff/role/{camp_id}/{role_id}", tags=["StaffInCamp"])
def update_role_staff(staffs_id:list[int], camp_id:int, role_id:int, db: Session = Depends(get_db)):
    staff = assign_role_staff(db, camp_id, staffs_id, role_id)
    return {"data": staff}