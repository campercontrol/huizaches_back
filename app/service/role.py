from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from crud.crud_role import (
    create_new_role,
    crud_update_role,
    get_all_role,
    get_role_by_uuid,
)
from model.user import User
from schema.role import RoleCreate, RoleModify
# from utils.check_role import chek_permission
from utils.db import SessionLocal
#from utils.functions_jwt import get_current_active_user

role_routes = APIRouter()

# Dependency


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@role_routes.get("/rol", tags=["Role"])
def get_role(
    is_active: boolean = True,
    db: Session = Depends(get_db),
):
    NAME = "get_role"

    list_rol = get_all_role(db, is_active)
    return {"data": list_rol}


@role_routes.post("/rol", tags=["Role"], status_code=200)
def create_role(
    role: RoleCreate, 
    response: Response, 
    db: Session = Depends(get_db)):
    NAME = "create_role"

    resultado = create_new_role(db, role)

    if resultado is not None:
        return {"mensaje": "Exitoso", "data": resultado}
    else:
        response.status_code = 401
        return {"mensaje": "No se pudo guardar en la BD", "data": resultado}


# @role_routes.post("/rol", tags=["Role"], status_code=200)
# def create_role_with_permissions(
#     role: RoleCreate,
#     response: Response,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_active_user),
# ):
#     NAME = "create_role_with_permissions"
#     chek_permission(db, current_user, NAME)

#     resultado = create_new_role(db, role)

#     all_endpoints = get_all_endpoint(db, True)

#     listOfReading = [Permission(row.id, resultado.id, False) for row in all_endpoints]

#     print(listOfReading)

#     crear_list_permissions(db, listOfReading)

#     if resultado is not None:
#         return {"mensaje": "Exitoso", "data": resultado}
#     else:
#         response.status_code = 401
#         return {"mensaje": "No se pudo guardar en la BD", "data": resultado}


@role_routes.get("/rol/{role_id}", tags=["Role"])
def get_role_by_id(
    role_id: str,
    db: Session = Depends(get_db),
):
    NAME = "get_role_by_id"
    #chek_permission(db, current_user, NAME)

    resultado = get_role_by_uuid(db, role_id)
    return {"data": resultado}


@role_routes.patch("/rol/{role_id}", tags=["Role"])
def update_role(
    role_id: str,
    role: RoleModify,
    response: Response,
    db: Session = Depends(get_db),
):
    NAME = "update_role"
    #chek_permission(db, current_user, NAME)

    update_data = role.dict(exclude_unset=True)
    respuesta_update_role = crud_update_role(db, role_id, update_data)

    if respuesta_update_role != 0:
        exist_role = get_role_by_uuid(db, role_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_role}
    else:
        response.status_code = 401
        return {"mensaje": "Ningun registro fue afectado", "data": ""}
