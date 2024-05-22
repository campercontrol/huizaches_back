from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.catalogs.staff_role_crud import (
    get_all_staff_role,
    get_staff_role_by_uuid,
    create_new_staff_role,
    update_staff_role_by_id,
    delete_staff_role
)
from schema.catalogs.staff_role_schema import(
    StaffRoleCreate,
    StaffRoleModify
)
from utils.db import SessionLocal

staff_role_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@staff_role_routes.get("/staff_role/", tags=["Catalogs"])
def get_staff_role(db: Session = Depends(get_db)):
    list_staff_role = get_all_staff_role(db)
    return {"data": list_staff_role}


@staff_role_routes.get("/staff_role/{staff_role_id}", tags=["Catalogs"])
def get_staff_role_by_id(staff_role_id:str,db: Session = Depends(get_db)):
    list_staff_role = get_staff_role_by_uuid(db,staff_role_id)
    return {"data": list_staff_role}


@staff_role_routes.post("/staff_role/", tags=["Catalogs"])
def create_staff_role(new_prueba:StaffRoleCreate,db: Session = Depends(get_db)):
    list_staff_role = create_new_staff_role(db,new_prueba)
    return {"data": list_staff_role}

@staff_role_routes.post("/staff_role/{staff_role_id}", tags=["Catalogs"])
def update_staff_role(staff_role_id:str,modify_staff_role:StaffRoleModify,db: Session = Depends(get_db)):

    update_data = modify_staff_role.dict(exclude_unset=True)
    print(update_data)
    staff_role_upcdate_result = update_staff_role_by_id(db,staff_role_id,update_data)

    if staff_role_upcdate_result != 0:
        exist_staff_role = get_staff_role_by_uuid(db, staff_role_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_staff_role}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@staff_role_routes.delete("/delete_staff_role/{staff_role_id}", tags=["Catalogs"])
def delete_staff_role_by_id(staff_role_id:int, db: Session = Depends(get_db)):
    response = delete_staff_role(db, staff_role_id)
    if response == None:
        raise HTTPException(status_code=404, detail="Licensed medicine not found")

    if response['status'] == 3:
        raise HTTPException(status_code=500, detail= response['detail'])
    return response    