from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response, BackgroundTasks, UploadFile
from sqlalchemy.orm import Session

from crud.crud_user import (
    get_all_user,
    create_new_user,
    get_user_by_uuid,
    crud_update_user_by_uuid,
    get_user_by_email,
    crud_update_user_by_email,
    search_user_by_email,
    update_password_all_users
)
from model.user import User
from schema.user import UserCreate, UserModify, UserResetPassword, UserChangePassword, UserChangeEmail

# from utils.check_role import chek_permission
from utils.db import SessionLocal
from utils.email_tools import send_simple_message
from utils.functions_jwt import generate_access_token_reset_pass, validate_token_general
from utils.hash import hash_str
from utils.image_tools import write_image

# from utils.functions_jwt import get_current_active_user

user_routes = APIRouter()

# Dependency


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@user_routes.get("/usuario", tags=["Usuarios"])
def get_users(is_active: boolean = True, db: Session = Depends(get_db)):
    NAME = "get_users"

    list_user = get_all_user(db, is_active)

    return {"data": list_user}


@user_routes.post("/usuario", tags=["Usuarios"], status_code=200)
def create_user(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    NAME = "create_user"

    revisar_correo = get_user_by_email(db, user.email)

    if revisar_correo:
        response.status_code = 401
        return {"mensaje": "Correo ya existente", "data": []}

    resultado = create_new_user(db, user)

    print("#=================")
    print(resultado)
    print("#=================")
    if resultado is not None:
        response.status_code = 200
        return {"mensaje": "Exitoso", "data": resultado}
    else:
        response.status_code = 401
        return {"mensaje": "No se pudo guardar en la BD", "data": resultado}


@user_routes.get("/usuario/{user_id}", tags=["Usuarios"])
def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
):
    NAME = "get_user_by_id"

    resultado = get_user_by_uuid(db, user_id)
    return {"data": resultado}


@user_routes.patch("/usuario/{user_id}", tags=["Usuarios"])
def update_user(
    user_id: str,
    user: UserModify,
    response: Response,
    db: Session = Depends(get_db),
):
    NAME = "update_user"

    update_data = user.dict(exclude_unset=True)
    print(update_data)
    exist_user = get_user_by_uuid(db, user_id)
    if not exist_user:
        response.status_code = 401
        return {"mensaje": "El usuario buscado no existe"}

    if "passw" in update_data:
        update_data["hashed_pass"] = hash_str(update_data["passw"])
        update_data.pop("passw")

    respuesta_update_user = crud_update_user_by_uuid(db, user_id, update_data)

    if respuesta_update_user != 0:
        exist_user = get_user_by_uuid(db, user_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_user}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}


@user_routes.post("/usuario/reset_password", tags=["Usuarios"])
def reset_password(
    user_reset: UserResetPassword, response: Response, db: Session = Depends(get_db)
):
    exist_email = get_user_by_email(db, user_reset.email)
    if not exist_email:
        response.status_code = 401
        return {"mensaje": "No email ingresado no esta registrado", "data": ""}
    elif not exist_email.is_active:
        response.status_code = 401
        return {"mensaje": "No email ingresado esta desactivado", "data": ""}
    else:
        accessToken = generate_access_token_reset_pass(user_reset.email)
        send_simple_message(
            "",
            [user_reset.email],
            "Reinicio de contraseña",
            f"""Porfavor entra a esta url para realizar el cambio de contraseña
            Url: 127.0.0.1/reset_password/?email={user_reset.email}&token={accessToken}
            """,
        )
        response.status_code = 200
        return {
            "mensaje": "Se ha enviado un correo con instrucciones para la recuperacion de su contraseña",
            "data": "",
        }


@user_routes.post("/usuario/change_password/{email}", tags=["Usuarios"])
def change_password(
    email: str,
    change_pass: UserChangePassword,
    response: Response,
    db: Session = Depends(get_db),
):
    status_code, resp_token = validate_token_general(change_pass.access_token)

    # Valida token
    if status_code == 403:
        response.status_code = 403
        respuesta = {
            "mensaje": "El tiempo para recuperar contraseña expiro",
            "data": [],
        }
        return respuesta
    elif status_code == 401:
        response.status_code = 401
        return resp_token

    # valida email de token y email enviado
    if email != resp_token["user_email"]:
        response.status_code = 401
        respuesta = {
            "mensaje": "El email no corresponde al token",
            "data": [],
        }
        return respuesta

    exist_email = get_user_by_email(db, email)

    if not exist_email:
        response.status_code = 401
        return {"mensaje": "No email ingresado no esta registrado", "data": ""}
    elif not exist_email.is_active:
        response.status_code = 401
        return {"mensaje": "No email ingresado esta desactivado", "data": ""}

    if change_pass.password != change_pass.password_confirm:
        response.status_code = 401
        respuesta = {
            "mensaje": "Ambas contraseñas no son iguales",
            "data": [],
        }
        return respuesta
    else:
        update_data = {"hashed_pass": hash_str(change_pass.password)}
        respuesta_update_user = crud_update_user_by_email(db, email, update_data)

        if respuesta_update_user != 0:
            response.status_code = 200
            return {
                "mensaje": "La contraseña se ha cambiado correctamente, lo proxima vez que inicie sesion podra usar su nueva contraseña",
                "data": [],
            }
        else:
            response.status_code = 401
            return {
                "mensaje": "Ocurrio un error inesperado, intente de nuevo",
                "data": "",
            }
        
@user_routes.post("/usuario/change_email/{email}", tags=["Usuarios"])
def change_email(
    email: str,
    change_pass: UserChangeEmail,
    response: Response,
    db: Session = Depends(get_db),
):
    status_code, resp_token = validate_token_general(change_pass.access_token)

    # Valida token
    if status_code == 403:
        response.status_code = 403
        respuesta = {
            "mensaje": "El tiempo para cambiar el correo expiro",
            "data": [],
        }
        return respuesta
    elif status_code == 401:
        response.status_code = 401
        return resp_token

    # valida email de token y email enviado
    if email != resp_token["user_email"]:
        response.status_code = 401
        respuesta = {
            "mensaje": "El email no corresponde al token",
            "data": [],
        }
        return respuesta

    exist_email = get_user_by_email(db, email)

    if not exist_email:
        response.status_code = 401
        return {"mensaje": "No email ingresado no esta registrado", "data": ""}
    elif not exist_email.is_active:
        response.status_code = 401
        return {"mensaje": "No email ingresado esta desactivado", "data": ""}

    if change_pass.email != change_pass.email_confirm:
        response.status_code = 401
        respuesta = {
            "mensaje": "Ambos correos no son iguales",
            "data": [],
        }
        return respuesta
    else:
        update_data = {"email": change_pass.email}
        respuesta_update_user = crud_update_user_by_email(db, email, update_data)

        if respuesta_update_user != 0:
            response.status_code = 200
            return {
                "mensaje": "El correo se ha cambiado correctamente, lo proxima vez que inicie sesion podra usar su nuevo correo",
                "data": [],
            }
        else:
            response.status_code = 401
            return {
                "mensaje": "Ocurrio un error inesperado, intente de nuevo",
                "data": "",
            }


        
@user_routes.get("/search/user/{search}", tags=["Usuarios"])
def get_search_user(search:str, db: Session = Depends(get_db)):
    possible_users  = search_user_by_email(db, search)
    return { "data": possible_users }


@user_routes.post("/update/all/password/", tags=["Usuaros"])
def update_all_users_pass(hash_pass:str, db: Session = Depends(get_db)):
    result = update_password_all_users(db, hash_pass)
    return {"data": result}