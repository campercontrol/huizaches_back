from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from model.catalogs import StaffRole
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_all_staff_role(db):
    rows = db.query(StaffRole).all()
    return rows

def get_staff_role_by_uuid(db, staff_role_id):
    return (
        db.query(StaffRole)
        .filter_by(
            id=staff_role_id,
        )
        .first()
    )


def create_new_staff_role(db, new_staff_role):
    db_staff_role = None
    try:
        db_staff_role = StaffRole(
            id=new_staff_role.id,
            name=new_staff_role.name,
            payment=new_staff_role.payment,
            color=new_staff_role.color,
            created_at=new_staff_role.created_at

        )
        db.add(db_staff_role)
        db.commit()
        db.refresh(db_staff_role)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_staff_role = None
        return db_staff_role
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_staff_role


def update_staff_role_by_id(db, staff_role_id, modify_staff_role):
    rows_updated = (
        db.query(StaffRole).filter_by(id=staff_role_id).update(modify_staff_role, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def delete_staff_role(db: Session, staff_role_id:int):
    staff_role = db.query(StaffRole).filter(StaffRole.id==staff_role_id).first()
    
    if staff_role == None:
        return None
    try:
        db.delete(staff_role)
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"status": 2, "detail": "Can not delete staff role, referenced by other table"}
    except:
        db.rollback()
        return {"status": 3, "detail": "Internal Server Error"}
    return {"status" : 1, "detail": "Staff role deleted successfully"}