from sqlalchemy.exc import SQLAlchemyError

from model.catalogs import Constant
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case, and_, or_


def get_all_constant(db):
    rows = db.query(Constant).all()
    return rows


def get_constant_by_uuid(db, constant_id):
    return (
        db.query(Constant)
        .filter_by(
            id=constant_id,
        )
        .first()
    )


def create_new_constant(db, new_constant):
    db_constant = None
    try:
        db_constant = Constant(
            id=new_constant.id,
            value=new_constant.value,
            num_id=new_constant.num_id,
            language=new_constant.language,
            model_name=new_constant.model_name,
            created_at=new_constant.created_at,
        )
        db.add(db_constant)
        db.commit()
        db.refresh(db_constant)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_constant = None
        return db_constant
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_constant


def update_constant_by_id(db, constant_id, modify_constant):
    rows_updated = (
        db.query(Constant)
        .filter_by(id=constant_id)
        .update(modify_constant, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_all_answer(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "answer", Constant.language == language)
        .all()
    )
    return rows


def get_all_assign_choice(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "assign_choice", Constant.language == language)
        .all()
    )
    return rows


def get_all_blood_type(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "blood_type", Constant.language == language)
        .all()
    )
    return rows

def get_all_blood_type_id_name(db, language: str = "es"):
    rows = (
        db.query(Constant.id, Constant.value)
        .filter(Constant.model_name == "blood_type", or_(Constant.language == "bi", Constant.language == language))
        .all()
    )
    return db_mapping_rows_to_dict(rows)



def get_all_camp_status(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "camp_status", Constant.language == language)
        .all()
    )
    return rows


def get_all_gender(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "gender", Constant.language == language)
        .all()
    )
    return rows


def get_all_gender_id_name(db, language: str = "es"):
    rows = (
        db.query(Constant.id, Constant.value)
        .filter(Constant.model_name == "gender", Constant.language == language)
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_all_grade(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "grade", Constant.language == language)
        .all()
    )
    return rows

def get_all_grade_id_name(db, language: str = "es"):
    rows = (
        db.query(Constant.id, Constant.value)
        .filter(Constant.model_name == "grade", Constant.language == "es")
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_all_med_auth(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "med_auth", Constant.language == language)
        .all()
    )
    return rows


def get_all_rol_colors(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "rol_colors", Constant.language == language)
        .all()
    )
    return rows


def get_all_triage(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "triage", Constant.language == language)
        .all()
    )
    return rows


def get_all_user_group(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "user_group", Constant.language == language)
        .all()
    )
    return rows

def get_all_email_template(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "email_template", Constant.language == language)
        .all()
    )
    return rows

def get_all_email_send_type(db, language: str = "es"):
    rows = (
        db.query(Constant)
        .filter(Constant.model_name == "send_type", Constant.language == language)
        .all()
    )
    return rows