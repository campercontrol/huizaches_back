from model.campers import Parent
from schema.campers.parent_schema import ParentCreate, ParentModify
from sqlalchemy import case, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict


def get_all_parent(db: Session):
    rows = db.query(Parent).all()
    return rows


def get_parent_by_uuid(db: Session, parent_id: int):
    return db.query(Parent).filter_by(id=parent_id).first()


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
    try:
        new_parent.user_id = user_id
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


def update_parent_by_id(db: Session, parent_id: int, modify_parent: ParentModify):
    rows_updated = (
        db.query(Parent)
        .filter_by(id=parent_id)
        .update(modify_parent, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


# def get_campers_from_parent


def delete_parent(db: Session, parent_id: int):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    db.delete(parent)
    db.commit()
    return {"status": True}


def search_parent_by_name(db: Session, search: str):
    possible_parent = (
        db.query(
            Parent.id,
            Parent.tutor_name,
            Parent.tutor_lastname_father,
            Parent.tutor_lastname_mother,
        )
        .filter(
            or_(
                Parent.tutor_name.ilike(r"%{}%".format(search)),
                Parent.tutor_lastname_father.ilike(r"%{}%".format(search)),
                Parent.tutor_lastname_mother.ilike(r"%{}%".format(search)),
            )
        )
        .all()
    )

    return db_mapping_rows_to_dict(possible_parent)
