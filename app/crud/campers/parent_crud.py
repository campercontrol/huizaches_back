from sqlalchemy.exc import SQLAlchemyError

from model.campers import Parent
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_parent(db):
    rows= db.query(Parent).all()
    return rows

def get_parent_by_uuid(db, parent_id):
    return(
        db.query(Parent)
        .filter_by(
            id=parent_id
        )
        .first()
    )

def create_new_parent(db, new_parent):
    db_parent = None
    try:
        db_parent = Parent(
            id = new_parent.id,
            tutor_name = new_parent.tutor_name,
            tutor_lastname_father = new_parent.tutor_lastname_father,
            tutor_lastname_mother = new_parent.tutor_lastname_mother,
            tutor_cellphone = new_parent.tutor_cellphone,
            tutor_home_phone = new_parent.tutor_home_phone,
            tutor_work_phone = new_parent.tutor_work_phone,
            contact_name = new_parent.contact_name,
            contact_lastname_father = new_parent.contact_lastname_father,
            contact_lastname_mother = new_parent.contact_lastname_mother,
            contact_cellphone = new_parent.contact_cellphone,
            contact_home_phone = new_parent.contact_home_phone,
            contact_work_phone = new_parent.contact_work_phone,
            contact_email = new_parent.contact_email,
            created_at = new_parent.created_at 
        )
        db.add(db_parent)
        db.commit()
        db.refresh(db_parent)
    except SQLALchemyError as e:
        print("#=================================#")
        print(e)
        print("#=================================#")
        db_parent = None
        return db_parent
    except Exception as e:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_parent

def update_parent_by_id(db, parent_id, modify_parent):
    rows_updated = (
        db.query(Parent).filter_by(id=parent_id).update(modify_parent, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

#def get_campers_from_parent