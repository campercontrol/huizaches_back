from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session

from crud.crud_user import (
    get_all_user,
    create_new_user,
    get_user_by_uuid,
    crud_update_user_by_uuid,
    get_user_by_email,
    crud_update_user_by_email,
    search_user_by_email,
    update_password_all_users,
    update_user_by_id,
    delete_user_by_id
)
from model.user import User
from schema.user import UserCreate, UserModify, UserResetPassword, UserChangePassword, UserChangeEmail
from model.staffs import Staff, StaffRecord
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

    check_email = get_user_by_email(db, user.email)

    if check_email:
        # return {"mensaje": "Correo ya existente", "data": []}
        return {"detail": {"status": 2, "msg": "Correo existente, no se puede crear el usuario"}}

    new_user = create_new_user(db, user)
    new_user_role = new_user.role_id

    if new_user_role == 1:
        pass
    if new_user_role == 2:
        current_season = 76
        try:
            staff_new_record = StaffRecord(
                attend = 0,
                attended = 0,
                total = 0
            )
            db.add(staff_new_record)
            db.commit()
            db.refresh(staff_new_record)

            default_prospect_profile = {
                "name": "Staff",
                "lastname_father": "default",
                "lastname_mother": "user",
                "photo": "media/tmp/default_user.png",
                "birthday": "2000-01-01",
                "curp": "CURP",
                "bio": "",
                "facebook": "default staff",
                "home_phone": "5555555555",
                "cellphone": "5555555555",
                "cv": "media/cv/default.pdf",
                "gender_id": 4,
                "record_id":staff_new_record.id,
                "season_id": current_season,
                "login_id": new_user.id,
                "coordinator": False,
                "employee_email_send": False,
                "employee": True,
            }  
            new_default_prospect_profile = Staff(**default_prospect_profile)
            db.add(new_default_prospect_profile)
            db.commit()
            db.refresh(new_default_prospect_profile)
        except Exception as e:
            print(e)
            db.delete(new_default_prospect_profile)
            db.delete(staff_new_record)
            db.delete(new_user)
            db.commit()
            raise HTTPException(status_code=500, detail={"status":3, "msg": "Internal server error"})

        return {"detail": {"status": 1, "msg": "Se ha creado correctamente el usuario"}}


    # print("#=================")
    # print(resultado)
    # print("#=================")
    # if resultado is not None:
    #     response.status_code = 200
    #     return {"mensaje": "Exitoso", "data": resultado}
    # else:
    #     response.status_code = 401
    #     return {"mensaje": "No se pudo guardar en la BD", "data": resultado}


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
    db: Session = Depends(get_db)
):
    response = update_user_by_id(db, user_id, user.dict())
    # if response == None:
    #     raise HTTPException(status_code=404, detail="User not found")
    if response['status'] == 3:
        raise HTTPException(status_code=500, detail=response)
    return {"detail": response}


# @user_routes.patch("/usuario/{user_id}", tags=["Usuarios"])
# def update_user(
#     user_id: str,
#     user: UserModify,
#     response: Response,
#     db: Session = Depends(get_db),
# ):
#     response = update_user_by_id(db, user_id, user)



#     # NAME = "update_user"

#     update_data = user.dict(exclude_unset=True)
#     print(update_data)
#     exist_user = get_user_by_uuid(db, user_id)
#     if not exist_user:
#         response.status_code = 401
#         return {"mensaje": "El usuario buscado no existe"}

#     if "passw" in update_data:
#         update_data["hashed_pass"] = hash_str(update_data["passw"])
#         update_data.pop("passw")

#     respuesta_update_user = crud_update_user_by_uuid(db, user_id, update_data)

#     if respuesta_update_user != 0:
#         exist_user = get_user_by_uuid(db, user_id)
#         return {"mensaje": "Actualizado Correctamente", "data": exist_user}
#     else:
#         return {"mensaje": "Ningun registro fue afectado", "data": ""}


@user_routes.post("/usuario/reset_password", tags=["Usuarios"])
def reset_password(
    user_reset: UserResetPassword, response: Response, db: Session = Depends(get_db)
):
    exist_email = get_user_by_email(db, user_reset.email)
    if not exist_email:
        response.status_code = 401
        return {"mensaje": "Email not registered", "data": ""}
    elif not exist_email.is_active:
        response.status_code = 401
        return {"mensaje": "Account is not active", "data": ""}
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

@user_routes.post("/user/verify/")
def verify_account(t: str, db: Session = Depends(get_db)):
    data = validate_token_general(t)
    if data[0] == 403:
        raise HTTPException(status_code=401, detail="Token Has expired") 
    if data[0] == 401:
        raise HTTPException(status_code=401, detail="Invalid token") 
    email = data[1]["user_email"]
    try:
        db.begin()
        account =  db.query(User).filter_by(email=email).first()
        account.is_active = True
        db.add(account)
        db.commit()
        db.refresh(account)
    except Exception as ex:
        db.rollback()
        print(ex)
        raise HTTPException(status_code=500, detail="Internal server error") 
    return {"detail": "The account was successfully verified"}

    
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


@user_routes.post("/update/all/password/", tags=["Usuarios"])
def update_all_users_pass(hash_pass:str, db: Session = Depends(get_db)):
    result = update_password_all_users(db, hash_pass)
    return {"data": result}

@user_routes.delete("/delete_usuario/{user_id}", tags=["Usuarios"])
def delete_user(user_id:str, db: Session = Depends(get_db)):
    response = delete_user_by_id(user_id)
    
    if response == None:
        raise HTTPException(status_code=404, detail="User not found")

    if response['status'] == 3:
        raise HTTPException(status_code=500, detail= response)
    return {"detail": response}    