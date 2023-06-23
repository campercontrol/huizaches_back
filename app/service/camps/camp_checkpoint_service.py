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
    delete_camp_checkpoint,
)

from crud.camps.camper_in_camp_crud import get_campers_subscribe_to_camp

from crud.campers.camper_checkpoint_crud import (
    get_camper_checkpoint_by_camper,
    get_camper_checkpoint_by_camper_check_id,
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


@camp_checkpoint_routes.get(
    "/camp_checkpoint/{camp_checkpoint_id}", tags=["CampCheckpoint"]
)
def get_camp_checkpoint_by_uid(camp_checkpoint_id: str, db: Session = Depends(get_db)):
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
        exist_camp_checkpoint = get_camp_checkpoint_by_id(db, camp_checkpoint_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_camp_checkpoint}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}


@camp_checkpoint_routes.get(
    "/camp_checkpoint_by_camp/{camp_id}", tags=["CampCheckpoint"]
)
def checkpoint_bycamp(camp_id, db: Session = Depends(get_db)):
    list_checkpoints = get_camp_checkpoint_by_camp(db, camp_id)
    return {"data": list_checkpoints}


@camp_checkpoint_routes.get("/camps_with_checkpoint/", tags=["CampCheckpoint"])
def camps_with_checkpoint(db: Session = Depends(get_db)):
    camps_checkpoint = get_camps_with_checkpoint(db)
    return {"data": camps_checkpoint}


@camp_checkpoint_routes.delete(
    "/delete_camp_checkpoint/{camp_checkpoint_id}", tags=["CampCheckpoint"]
)
def delete_checkpoint_by_id(camp_checkpoint_id: int, db: Session = Depends(get_db)):
    status = delete_camp_checkpoint(db, camp_checkpoint_id)
    return {"status": status}


@camp_checkpoint_routes.get(
    "/camp_checkpoint_module/{camp_id}", tags=["CampCheckpoint"]
)
def get_camp_checkpoint_module(camp_id: int, db: Session = Depends(get_db)):
    data = []
    campers_list = get_campers_subscribe_to_camp(db, camp_id)
    for camper in campers_list:
        all_checks = []
        camper_checks = []
        camper_checkpoints = get_camper_checkpoint_by_camper(db, camper.camper_id)
        for camper_check in camper_checkpoints:
            camper_checks.append(getattr(camper_check, "checkpoint_id"))
        camp_checks = get_camp_checkpoint_by_camp(db, camp_id)

        for camp_check in camp_checks:
            if getattr(camp_check, "id") in camper_checks:
                camper_check_case = get_camper_checkpoint_by_camper_check_id(
                    db, camper.camper_id, getattr(camp_check, "id")
                )
                all_checks.append(
                    {
                        "checkpoint_id": camp_check.id,
                        "checkpoint_date": camper_check_case.checkin_date,
                        "checkpoint_check": True,
                    }
                )
            else:
                all_checks.append(
                    {
                        "checkpoint_id": camp_check.id,
                        "checkpoint_date": False,
                        "checkpoint_check": False,
                    }
                )

        data.append({"camper": camper, "checkpoints": all_checks})

    return {
        "data": data,
    }
