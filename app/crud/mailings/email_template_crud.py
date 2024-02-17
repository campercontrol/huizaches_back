from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from model.mailings import EmailTemplate
from model.catalogs import Constant
from schema.mailings.email_template_schema import (
    EmailTemplateCreate,
    EmailTemplateModify,
)
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case, and_


def get_all_email_template(db):
    rows = db.query(EmailTemplate).all()
    return rows


def get_email_template_by_uuid(db, email_template_id):
    return (
        db.query(EmailTemplate)
        .filter_by(
            id=email_template_id,
        )
        .first()
    )


def create_new_email_template(db, new_email_template: EmailTemplateCreate):
    db_email_template = None
    try:
        db_email_template = EmailTemplate(**new_email_template.dict())
        db.add(db_email_template)
        db.commit()
        db.refresh(db_email_template)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_email_template = None
        return db_email_template
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_email_template


def update_email_template_by_id(
    db, email_template_id, modify_email_template: EmailTemplateModify
):
    rows_updated = (
        db.query(EmailTemplate)
        .filter_by(id=email_template_id)
        .update(modify_email_template, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def delete_email_template(db: Session, email_template_id: int):
    email_template = (
        db.query(EmailTemplate).filter(EmailTemplate.id == email_template_id).first()
    )
    db.delete(email_template)
    db.commit()
    return {"status": True}


def get_all_massive_template(db: Session):
    return db_mapping_rows_to_dict(
        (
            db.query(EmailTemplate.id, EmailTemplate.title)
            .filter(EmailTemplate.template_type == 41)
            .all()
        )
    )


def get_all_system_template(db: Session):
    return db_mapping_rows_to_dict(
        (
            db.query(EmailTemplate.id.label("id"), Constant.value.label("title"))
            .join(Constant, EmailTemplate.template_type == Constant.id)
            .filter(
                EmailTemplate.template_type!=41
            )
            .all()
        )
    )
