from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from crud.crud_permission import (
    get_all_permission,
    create_new_permission,
    get_permission_by_uuid,
    crud_update_permission
)
from model.user import User
from schema.permission import PermissionCreate,PermissionModify 
# from utils.check_role import chek_permission
from utils.db import SessionLocal
#from utils.functions_jwt import get_current_active_user

permission_routes = APIRouter()

# Dependency


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@permission_routes.get("/permisos", tags=["Permission"])
def get_permission(
    is_active: boolean = True,
    db: Session = Depends(get_db),
):
    NAME = "get_permission"

    list_rol = get_all_permission(db, is_active)
    return {"data": list_rol}


@permission_routes.post("/permisos", tags=["Permission"], status_code=200)
def create_permission(
    permission: PermissionCreate, 
    response: Response, 
    db: Session = Depends(get_db)):
    NAME = "create_permission"

    resultado = create_new_permission(db, permission)

    if resultado is not None:
        return {"mensaje": "Exitoso", "data": resultado}
    else:
        response.status_code = 401
        return {"mensaje": "No se pudo guardar en la BD", "data": resultado}


@permission_routes.get("/permisos/{permission_id}", tags=["Permission"])
def get_permission_by_id(
    permission_id: str,
    db: Session = Depends(get_db),
):
    NAME = "get_permission_by_id"
    #chek_permission(db, current_user, NAME)

    resultado = get_permission_by_uuid(db, permission_id)
    return {"data": resultado}


@permission_routes.patch("/permisos/{permission_id}", tags=["Permission"])
def update_role(
    permission_id: str,
    permission: PermissionModify,
    response: Response,
    db: Session = Depends(get_db),
):
    NAME = "update_role"
    #chek_permission(db, current_user, NAME)

    update_data = permission.dict(exclude_unset=True)
    respuesta_update_permission = crud_update_permission(db, permission_id, update_data)

    if respuesta_update_permission != 0:
        exist_role = get_permission_by_uuid(db, permission_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_role}
    else:
        response.status_code = 401
        return {"mensaje": "Ningun registro fue afectado", "data": ""}
