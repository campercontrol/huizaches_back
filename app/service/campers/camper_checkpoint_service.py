from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.campers.camper_checkpoint_crud import (
    get_all_camper_checkpoint,
    get_camper_checkpoint_by_id,
    get_camper_checkpoint_by_camper,
    create_new_camper_checkpoint,
    update_camper_checkpoint_by_id,
)

from schema.campers.camper_checkpoint_schema import (
    CamperCheckpointCreate,
    CamperCheckpointModify,
)
from utils.db import SessionLocal

camper_checkpoint_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@camper_checkpoint_routes.get("/camper_checkpoint/", tags=["CamperCheckpoint"])
def get_camper_checkpoint(db: Session = Depends(get_db)):
    list_camper_checkpoint = get_all_camper_checkpoint(db)
    return {"data": list_camper_checkpoint}


@camper_checkpoint_routes.get("/camper_checkpoint/{camper_checkpoint_id}", tags=["CamperCheckpoint"])
def get_camper_checkpoint_by_uid(
    camper_checkpoint_id: str, db: Session = Depends(get_db)
):
    list_camper_checkpoint = get_camper_checkpoint_by_id(db, camper_checkpoint_id)
    return {"data": list_camper_checkpoint}


@camper_checkpoint_routes.post("/camper_checkpoint/", tags=["CamperCheckpoint"])
def create_camper_checkpoint(
    new_camper_checkpoint: CamperCheckpointCreate, db: Session = Depends(get_db)
):
    list_camper_checkpoint = create_new_camper_checkpoint(db, new_camper_checkpoint)
    return {"data": list_camper_checkpoint}


@camper_checkpoint_routes.patch(
    "/camper_checkpoint/{camper_checkpoint_id}", tags=["CamperCheckpoint"]
)
def update_camper_checkpoint(
    camper_checkpoint_id: int,
    modify_camper_checkpoint: CamperCheckpointModify,
    db: Session = Depends(get_db),
):
    update_data = modify_camper_checkpoint.dict(exclude_unset=True)
    print(update_data)
    camp_checkpoint_update_result = update_camper_checkpoint_by_id(
        db, camper_checkpoint_id, update_data
    )

    if camp_checkpoint_update_result != 0:
        exist_camp_checkpoint = get_camper_checkpoint_by_id(
            db, camper_checkpoint_id
        )
        return {"mensaje": "Actualizado Correctamente", "data": exist_camp_checkpoint}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}

@camper_checkpoint_routes.get("/camper_checkpoint_by_camp/{camp_id}", tags=["CamperCheckpoint"])
def checkpoint_by_camper(camper_id, db: Session = Depends(get_db)):
    list_checkpoints = get_camper_checkpoint_by_camper(db, camper_id)
    return{"data": list_checkpoints}