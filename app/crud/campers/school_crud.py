from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from model.campers import School
from crud.crud_user import create_new_user
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case
from schema.user import UserCreate

def get_all_school(db):
    rows= db.query(School).all()
    return rows

def get_school_by_uuid(db, school_id):
    return(
        db.query(School)
        .filter_by(
            id=school_id
        )
        .first()
    )

def create_new_school(db, new_school):
    db_school = None
    
    new_user_obj = UserCreate(
        email=new_school.email,
        passw=new_school.password,
        role_id=3,
        is_superuser=False
    )
    new_school_user = create_new_user(db, new_user_obj)
    try:
        db_school = School(
            id=new_school.id,
            login_id=new_school_user.id,
            name=new_school.name,
            address = new_school.address,
            url = new_school.url,
            contact = new_school.contact,
            phone = new_school.phone,
            cellphone = new_school.cellphone,
            email = new_school.email,
            contact_second_name = new_school.contact_second_name,
            contact_second_phone = new_school.contact_second_phone,
            contact_second_cellphone = new_school.contact_second_cellphone,
            contact_second_email = new_school.contact_second_email,
            contact_third_name = new_school.contact_third_name,
            contact_third_phone = new_school.contact_third_phone,
            contact_third_cellphone = new_school.contact_third_cellphone,
            contact_third_email = new_school.contact_third_email,
            verify = new_school.verify,
            active = new_school.active,
            created_at = new_school.created_at 
        )
        db.add(db_school)
        db.commit()
        db.refresh(db_school)
    except SQLAlchemyError as e:
        db.rollback()
        print("#=================================#")
        print(e)
        print("#=================================#")
        db_school = None
        return db_school
    except Exception as e:
        db.rollback()
        print(f"No se pudo guardar en la base de datos: {e}")
    return db_school

def update_school_by_id(db, school_id, modify_school):
    rows_updated = (
        db.query(School).filter_by(id=school_id).update(modify_school, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def get_active_school(db):
    rows= db.query(School.id, School.name).filter_by(active=True).all()
    return db_mapping_rows_to_dict(rows)

def delete_school(db: Session, school_id:int):
    school = db.query(School).filter(School.id==school_id).first()
    db.delete(school)
    db.commit()
    return {"status" : True}

