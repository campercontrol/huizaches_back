from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.staffs.staff_crud import (
    get_all_prospect,
    create_new_prospect,
    accept_prospect,
    delete_prospect,
    staff_dashboard,
    get_staff_by_id
)

from schema.staffs.staff_schema import (
    ProspectCompleteCreate    
)

from crud.crud_user import create_new_user
from utils.db import SessionLocal

staff_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@staff_routes.get("/prospect/", tags=["Prospect"])
def get_prospects(db: Session = Depends(get_db)):
    list_prospect = get_all_prospect(db)
    return {"data": list_prospect}

@staff_routes.post("/prospect/", tags=["Prospect"])
def create_prospect(
    new_prospect: ProspectCompleteCreate, db: Session = Depends(get_db)
):
    user = create_new_user(db, new_prospect.user)
    prospect = create_new_prospect(db, new_prospect.prospect, user.id)
    return {"data": prospect}

@staff_routes.patch("/accept_prospect/{prospect_id}", tags=["Prospect"])
def accept_prospecto_to_staff(prospect_id:int, db: Session = Depends(get_db)):
    status = accept_prospect(db, prospect_id)
    return {"data": status}

@staff_routes.delete("/delete_prospect/{prospect_id}", tags=["Prospect"])
def delete_prospect_by_id(prospect_id:int, db:Session = Depends(get_db)):
    status = delete_prospect(db, prospect_id)
    return {"status" : status}

@staff_routes.get("/staff_dashboard/{staff_id}", tags = ["Staff"])
def get_staff_dashboard(staff_id:int, db:Session = Depends(get_db)):
    staff_dashboard_info = staff_dashboard(db, staff_id)
    return{"data": staff_dashboard_info}

@staff_routes.get("/staff/{staff_id}", tags = ["Staff"])
def get_staff_profile(staff_id:int, db:Session = Depends(get_db)):
    staff = get_staff_by_id(db, staff_id)
    return{"data": staff}