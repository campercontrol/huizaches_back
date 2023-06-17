from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.camps.camp_checkpoint_crud import (
    get_all_camp_checkpoint,
    get_camp_checkpoint_by_id,
    get_camp_checkpoint_by_camp,
    create_new_camp_checkpoint,
    update_camp_checkpoint_by_id,
    get_camps_with_checkpoint,
    delete_camp_checkpoint
)

from crud.camps.camper_in_camp_crud import (
    get_campers_subscribe_to_camp
)

from crud.campers.camper_checkpoint_crud import (
    get_camper_checkpoint_by_camper
)

from schema.camps.camp_checkpoint_schema import (
    CampCheckpointCreate,
    CampCheckpointModify,
)
from utils.db import SessionLocal

camp_checkpoint_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@camp_checkpoint_routes.get("/camp_checkpoint/", tags=["CampCheckpoint"])
def get_camp_checkpoint(db: Session = Depends(get_db)):
    list_camp_checkpoint = get_all_camp_checkpoint(db)
    return {"data": list_camp_checkpoint}


@camp_checkpoint_routes.get("/camp_checkpoint/{camp_checkpoint_id}", tags=["CampCheckpoint"])
def get_camp_checkpoint_by_uid(
    camp_checkpoint_id: str, db: Session = Depends(get_db)
):
    list_camp_checkpoint = get_camp_checkpoint_by_id(db, camp_checkpoint_id)
    return {"data": list_camp_checkpoint}


@camp_checkpoint_routes.post("/camp_checkpoint/", tags=["CampCheckpoint"])
def create_camp_checkpoint(
    new_camp_checkpoint: CampCheckpointCreate, db: Session = Depends(get_db)
):
    list_camp_checkpoint = create_new_camp_checkpoint(db, new_camp_checkpoint)
    return {"data": list_camp_checkpoint}


@camp_checkpoint_routes.patch(
    "/camp_checkpoint/{camp_checkpoint_id}", tags=["CampCheckpoint"]
)
def update_camp_checkpoint(
    camp_checkpoint_id: int,
    modify_camp_checkpoint: CampCheckpointModify,
    db: Session = Depends(get_db),
):
    update_data = modify_camp_checkpoint.dict(exclude_unset=True)
    print(update_data)
    camp_checkpoint_update_result = update_camp_checkpoint_by_id(
        db, camp_checkpoint_id, update_data
    )

    if camp_checkpoint_update_result != 0:
        exist_camp_checkpoint = get_camp_checkpoint_by_id(
            db, camp_checkpoint_id
        )
        return {"mensaje": "Actualizado Correctamente", "data": exist_camp_checkpoint}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@camp_checkpoint_routes.get("/camp_checkpoint_by_camp/{camp_id}", tags=["CampCheckpoint"])
def checkpoint_bycamp(camp_id, db: Session = Depends(get_db)):
    list_checkpoints = get_camp_checkpoint_by_camp(db, camp_id)
    return{"data": list_checkpoints}

@camp_checkpoint_routes.get("/camps_with_checkpoint/", tags= ["CampCheckpoint"])
def camps_with_checkpoint(db: Session = Depends(get_db)):
    camps_checkpoint = get_camps_with_checkpoint(db)
    return{"data": camps_checkpoint} 

@camp_checkpoint_routes.delete("/delete_camp_checkpoint/{camp_checkpoint_id}", tags=["CampCheckpoint"])
def delete_checkpoint_by_id(camp_checkpoint_id:int, db: Session = Depends(get_db)):
    status = delete_camp_checkpoint(db, camp_checkpoint_id)
    return{"status": status}

@camp_checkpoint_routes.get("/camp_checkpoint_module/{camp_id}", tags=["CampCheckpoint"])
def get_camp_checkpoint_module(camp_id:int, db: Session = Depends(get_db)):

    campers_list= get_campers_subscribe_to_camp(db, camp_id)
    camper_checks = []
    for camper in campers_list:
        camper_checkpoint = get_camper_checkpoint_by_camper(db, camper.camper_id)
        camper_checks.append(camper_checkpoint)

    return{
        "campers": campers_list,
        "campers_checkpoint": camper_checks
    } 
