from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.staffs.staff_crud import (
    get_all_prospect,
    create_new_prospect
)

from schema.staffs.staff_schema import (
    ProspectCreate    
)
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
    new_prospect: ProspectCreate, db: Session = Depends(get_db)
):
    list_prospect = create_new_prospect(db, new_prospect)
    return {"data": list_prospect}
