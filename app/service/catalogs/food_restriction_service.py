from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.catalogs.food_restriction_crud import (
    get_all_food_restriction,
    get_food_restriction_by_uuid,
    create_new_food_restriction,
    update_food_restriction_by_id,
    delete_food_restriction
)
from schema.catalogs.food_restriction_schema import(
    FoodRestrictionCreate,
    FoodRestrictionModify
)
from utils.db import SessionLocal

food_restriction_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@food_restriction_routes.get("/food_restriction/", tags=["Catalogs"])
def get_food_restriction(db: Session = Depends(get_db)):
    list_food_restriction = get_all_food_restriction(db)
    return {"data": list_food_restriction}


@food_restriction_routes.get("/food_restriction/{food_restriction_id}", tags=["Catalogs"])
def get_food_restriction_by_id(food_restriction_id:str,db: Session = Depends(get_db)):
    list_food_restriction = get_food_restriction_by_uuid(db,food_restriction_id)
    return {"data": list_food_restriction}


@food_restriction_routes.post("/food_restriction/", tags=["Catalogs"])
def create_food_restriction(new_prueba:FoodRestrictionCreate,db: Session = Depends(get_db)):
    list_food_restriction = create_new_food_restriction(db,new_prueba)
    return {"data": list_food_restriction}

@food_restriction_routes.post("/food_restriction/{food_restriction_id}", tags=["Catalogs"])
def update_food_restriction(food_restriction_id:str,modify_food_restriction:FoodRestrictionModify,db: Session = Depends(get_db)):

    update_data = modify_food_restriction.dict(exclude_unset=True)
    print(update_data)
    food_restriction_upcdate_result = update_food_restriction_by_id(db,food_restriction_id,update_data)

    if food_restriction_upcdate_result != 0:
        exist_food_restriction = get_food_restriction_by_uuid(db, food_restriction_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_food_restriction}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@food_restriction_routes.delete("/delete_food_restriction/{food_restriction_id}", tags=["Catalogs"])
def delete_food_restriction_by_id(food_restriction_id:int, db: Session = Depends(get_db)):
    status = delete_food_restriction(db, food_restriction_id)
    return{"status": status}