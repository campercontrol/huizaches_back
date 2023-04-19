from sqlalchemy.exc import SQLAlchemyError

from model.campers import School
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


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
    try:
        db_school = School(
            id=new_school.id,
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
    except SQLALchemyError as e:
        print("#=================================#")
        print(e)
        print("#=================================#")
        db_school = None
        return db_school
    except Exception as e:
        print(f"No se pudo guardar en la base de datos: {ex}")
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