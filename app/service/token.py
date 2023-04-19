from datetime import datetime, timedelta
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from crud.crud_user import get_user_by_email
from schema.token import Token, TokenRefresh
from utils.db import SessionLocal
from utils.functions_jwt import validate_token,create_access_token,generate_new_tokens
from utils.hash import verify_str_hash

SECRET_KEY = "39d87423287d550c71e16d02fa7c4a522752a20bed9c505740b13aceeab5bf8a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 35

token_routes = APIRouter()

# Dependency


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def authenticate_user(db, username: str, password: str):
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not verify_str_hash(password, user.hashed_pass):
        return False
    return user


# def get_permissions_menu(db, user):
#     permissions_list = get_permissions_by_role_uuid_by_active(db, user.role_id, True)
#     list_menu_permission = []
#     for i in permissions_list:
#         path_arr = i.description.split("/")
#         try:
#             path = f"/{path_arr[1]}"
#             if path not in list_menu_permission:
#                 list_menu_permission.append(path)
#             else:
#                 pass
#         except Exception as ex:
#             print(ex)
#     return list_menu_permission


@token_routes.post("/token", response_model=Token, tags=["Token"])
async def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    #path_menu_permissions = get_permissions_menu(db, user)

    # print(">>>>>")
    # print(path_menu_permissions)
    # print(">>>>>")

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    refresh_token = create_access_token(
        data={"sub": user.email},
        expires_delta=refresh_token_expires,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@token_routes.post("/refresh/token", tags=["Token"])
async def refresh_access_token(
    token_refresh_data: TokenRefresh,
    db: Session = Depends(get_db),
    response: Response = 200,
):
    status_token, respuesta = validate_token(token_refresh_data.access_token)
    # print(">>>>>>>>>>>")
    # print(status_token)
    # print(respuesta)
    # print(">>>>>>>>>>>")

    if status_token == 403:
        # realiza Verificacion del token Refresh
        response.status_code = 403
        status_token, respuesta = validate_token(token_refresh_data.refresh_token)
        if status_token == 403:
            response.status_code = 401
            respuesta = {
                "mensaje": "Ambos tokens estan expirados, no se puede refrescar",
                "data": [],
            }
        elif status_token == 200:
            response.status_code = 200
            respuesta = generate_new_tokens(db, respuesta.username)
        else:
            response.status_code = 401
    elif status_token == 200:
        # print(respuesta.username)
        respuesta = generate_new_tokens(db, respuesta.username)
    else:
        response.status_code = 401

    return respuesta
