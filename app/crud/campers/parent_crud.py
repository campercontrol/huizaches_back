from model.campers import Parent
from model.user import User
from model.campers import Camper
from helper.parent_helpers import append_campers_for_parent_admin
from schema.campers.parent_schema import ParentCreate, ParentModify
from crud.campers.camper_crud import get_campers_from_parent
from sqlalchemy import case, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.db import db_mapping_rows_to_dict
from helper.mailing_helpers import send_mail_parent
from utils.toku_payment_tools import create_customer

import json


def get_all_parent(db: Session):
    rows = db.query(Parent).all()
    return rows


def get_parent_by_uuid(db: Session, parent_id: int):
    return db.query(Parent).filter_by(id=parent_id).first()


def get_parent_for_admin_by_id(db: Session, parent_id: int):
    parent = (
        db.query(
            User.id.label("user_id"),
            User.email.label("user_email"),
            Parent.id.label("tutor_id"),
            Parent.tutor_name.label("tutor_name"),
            Parent.tutor_lastname_father.label("tutor_lastname_father"),
            Parent.tutor_lastname_mother.label("tutor_lastname_mother"),
            Parent.tutor_cellphone.label("tutor_cellphone"),
            Parent.tutor_home_phone.label("tutor_home_phone"),
            Parent.tutor_work_phone.label("tutor_work_phone"),
            Parent.contact_name.label("contact_name"),
            Parent.contact_lastname_father.label("contact_lastname_father"),
            Parent.contact_lastname_mother.label("contact_lastname_mother"),
            Parent.contact_cellphone.label("contact_cellphone"),
            Parent.contact_home_phone.label("contact_home_phone"),
            Parent.contact_work_phone.label("contact_work_phone"),
            Parent.contact_email.label("contact_email"),
        )
        .outerjoin(User, User.id == Parent.user_id)
        .filter(Parent.id == parent_id)
        .all()
    )
    if parent:
        return db_mapping_rows_to_dict(parent)[0]
    else:
        return "Parent doesn't exist"


def create_new_parent(db, new_parent: ParentCreate):
    db_parent = None
    try:
        db_parent = Parent(**new_parent.dict())
        db.add(db_parent)
        db.commit()
        db.refresh(db_parent)
    except SQLAlchemyError as e:
        print("#=================================#")
        print(e)
        print("#=================================#")
        db_parent = None
        return db_parent
    except Exception as e:
        print(f"No se pudo guardar en la base de datos: {e}")
    return db_parent


def create_new_parent_user_id(db, new_parent: ParentCreate, user_id: int):
    db_parent = None
    email_welcome_template = 16
    try:
        new_parent.user_id = user_id
        user = db.query(User).filter(User.id == user_id).first()
        db_parent = Parent(**new_parent.dict())
        db.add(db_parent)
        db.commit()
        db.refresh(db_parent)
        send_mail_parent(db, [user.email, db_parent.contact_email], email_welcome_template, user, db_parent)
    except Exception as e:
        db.delete(db_parent)
        db.delete(user)
        db.commit()
        print(e)
        raise HTTPException(status_code=500, detail="Ocurrió un error al crear el padre")
    
    return db_parent


def update_parent_by_id(db: Session, parent_id: int, modify_parent: ParentModify):
    rows_updated = (
        db.query(Parent)
        .filter_by(id=parent_id)
        .update(modify_parent, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_parent_by_camper_id(db, camper_id):
    
    query = db.query(Parent.tutor_name.label("name"),
                     Parent.id,
                     Parent.tutor_lastname_father.label("lastname_father"),
                     Parent.tutor_lastname_mother.label("lastname_mother"),
                     User.email).join(User, User.id == Parent.user_id).join(Camper, Camper.parent_id == Parent.id).filter(Camper.id == camper_id)
    data = db.execute(query)
    return data.mappings().first()
 
    


def delete_parent(db: Session, parent_id: int):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    db.delete(parent)
    db.commit()
    return {"status": True}


def search_parent_by_name_user(db: Session, search: str):
    parents = (
        db.query(
            User.id.label("user_id"),
            Parent.id.label("tutor_id"),
            Parent.tutor_name.label("tutor_name"),
            Parent.tutor_lastname_father.label("tutor_lastname_father"),
            Parent.tutor_lastname_mother.label("tutor_lastname_mother"),
            Parent.tutor_home_phone.label("tutor_home_phone"),
            Parent.tutor_work_phone.label("tutor_work_phone"),
            Parent.tutor_cellphone.label("tutor_cellphone"),
            User.email.label("tutor_email"),
            Parent.contact_email.label("second_tutor_email"),
        )
        .outerjoin(User, User.id == Parent.user_id)
        .filter(
            or_(
                Parent.tutor_name.ilike(r"%{}%".format(search)),
                Parent.contact_email.ilike(r"%{}%".format(search)),
                Parent.tutor_lastname_father.ilike(r"%{}%".format(search)),
                Parent.tutor_lastname_mother.ilike(r"%{}%".format(search)),
                User.email.ilike(r"%{}%".format(search)),
            )
        )
        .all()
    )

    if parents:
        possible_parents = append_campers_for_parent_admin(db, parents)
    else:
        possible_parents = []

    return possible_parents


def get_all_parent_admin(db: Session):
    parents = (
        db.query(
            User.id.label("user_id"),
            Parent.id.label("tutor_id"),
            Parent.tutor_name.label("tutor_name"),
            Parent.tutor_lastname_father.label("tutor_lastname_father"),
            Parent.tutor_lastname_mother.label("tutor_lastname_mother"),
            Parent.tutor_home_phone.label("tutor_home_phone"),
            Parent.tutor_work_phone.label("tutor_work_phone"),
            Parent.tutor_cellphone.label("tutor_cellphone"),
            User.email.label("tutor_email"),
            Parent.contact_email.label("second_tutor_email"),
        )
        .outerjoin(User, User.id == Parent.user_id)
        .all()
    )

    if parents:
        possible_parents = append_campers_for_parent_admin(db, parents)
    else:
        possible_parents = "Data not found"

    return possible_parents
