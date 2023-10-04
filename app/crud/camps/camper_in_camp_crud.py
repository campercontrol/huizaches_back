from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import CamperInCamp, Camp, Location, CampExtraCharge, CampExtraQuestion
from model.campers import Camper, CamperRecord, Parent, School, CamperExtraAnswer
from model.payments import CamperExtraCharge
from model.catalogs import Constant
from model.user import User
from schema.camps.camper_in_camp_schema import (
    CamperInCampCreate,
    CamperInCampModify,
)


def get_all_camper_in_camp(db: Session):
    rows = db.query(CamperInCamp).all()
    return rows


def create_new_camper_in_camp(db: Session, new_camper_in_camp: CamperInCampCreate):
    db_camper_in_camp = None
    try:
        camp_price = (
            db.query(Camp.public_price).filter_by(id=new_camper_in_camp.camp_id).first()
        )
        db_camper_in_camp = CamperInCamp(
            camp_id=new_camper_in_camp.camp_id,
            status=new_camper_in_camp.status,
            payment_balance=getattr(camp_price, "public_price"),
            camper_id=new_camper_in_camp.camper_id,
        )
        db.add(db_camper_in_camp)
        db.commit()
        db.refresh(db_camper_in_camp)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_in_camp = None
        return db_camper_in_camp
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_in_camp


def update_camper_in_camp_by_id(
    db: Session,
    camp_id: int,
    camper_id: int,
    modify_camper_in_camp: CamperInCampModify,
):
    print("######################################################")
    print(type(modify_camper_in_camp))
    rows_updated = (
        db.query(CamperInCamp)
        .filter(
            and_(CamperInCamp.camp_id == camp_id, CamperInCamp.camper_id == camper_id)
        )
        .update(modify_camper_in_camp, synchronize_session="fetch")
    )
    print(rows_updated)
    db.commit()
    return rows_updated


def get_subscribe_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camper.id.label("camper_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
            CamperInCamp.payment_balance.label("camper_payment_balance"),
        )
        .join(Camp, CamperInCamp.camp_id == Camp.id)
        .join(Camper, CamperInCamp.camper_id == Camper.id)
        .join(Constant, CamperInCamp.status == Constant.id)
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.status == 36,
                Camp.active == True,
                Camp.start >= date.today(),
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_cancelled_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
            CamperInCamp.payment_balance.label("camper_payment_balance"),
        )
        .join(Camp, CamperInCamp.camp_id == Camp.id)
        .join(Constant, CamperInCamp.status == Constant.id)
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.status == 37,
                Camp.active == True,
                Camp.start >= date.today(),
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_all_cancelled_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
            CamperInCamp.payment_balance.label("camper_payment_balance"),
        )
        .join(Camp, CamperInCamp.camp_id == Camp.id)
        .join(Constant, CamperInCamp.status == Constant.id)
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.status == 37,
                Camp.active == True,
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_past_subscribe_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            Camp.id.label("camp_id"),
            Camp.name.label("camp_name"),
            Camp.start.label("camp_start"),
            Camp.end.label("camp_end"),
            Location.name.label("location_name"),
            Camp.public_price.label("public_price"),
            CamperInCamp.payment_balance.label("camper_payment_balance"),
        )
        .join(Camp, CamperInCamp.camp_id == Camp.id)
        .join(Constant, CamperInCamp.status == Constant.id)
        .join(Location, Camp.location_id == Location.id)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.status == 36,
                Camp.active == True,
                Camp.start < date.today(),
            )
        )
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_camper_in_camp_by_camper_camp(db: Session, camper_id: int, camp_id: int):
    camper_in_camp = (
        db.query(CamperInCamp)
        .filter(
            and_(
                CamperInCamp.camper_id == camper_id,
                CamperInCamp.camp_id == camp_id,
                CamperInCamp.status == 36,
            )
        )
        .first()
    )
    if camper_in_camp:
        return camper_in_camp
    else:
        return False


def get_campers_for_module(db: Session, camp_id: int):
    campers = (
        db.query(
            Camper.id.label("camper_id"),
            Camper.name.label("camper_name"),
            Camper.lastname_father.label("camper_lastname_father"),
            Camper.lastname_mother.label("camper_lastname_mother"),
        )
        .join(CamperInCamp, CamperInCamp.camper_id == Camper.id)
        .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36))
        .all()
    )
    return db_mapping_rows_to_dict(campers)


def get_camps_name_amount_camper(db: Session, camper_id: int):
    data = []
    camps = get_subscribe_by_camper(db, camper_id)
    cancelled_camps = get_all_cancelled_by_camper(db, camper_id)

    for camp in camps:
        data.append(
            {
                "camp_id": getattr(camp, "camp_id"),
                "camp_name": getattr(camp, "camp_name"),
                "camper_payment_balance": getattr(camp, "camper_payment_balance"),
            }
        )

    for camp in cancelled_camps:
        if getattr(camp, "camper_payment_balance") > 0:
            data.append(
                {
                    "camp_id": getattr(camp, "camp_id"),
                    "camp_name": getattr(camp, "camp_name"),
                    "camper_payment_balance": getattr(camp, "camper_payment_balance"),
                }
            )
    return data


def get_campers_for_camp(db: Session, camp_id: int):
    campers = (
        db.query(
            CamperInCamp.id.label("camper_in_camp_id"),
            Camper.record_id.label("camper_record_id"),
            CamperRecord.id.label("record_id"),
            Camper.id.label("camper_id"),
            Camper.photo.label("camper_photo"),
            (
                Camper.name
                + " "
                + Camper.lastname_father
                + " "
                + Camper.lastname_mother
            ).label("camper_full_name"),
            CamperRecord.attend.label("camper_attend"),
            CamperRecord.attended.label("camper_attended"),
            CamperRecord.total.label("camper_total"),
            CamperInCamp.payment_balance.label("camper_total_balance"),
            Camper.birthday.label("camper_birthday"),
            (
                Parent.tutor_name
                + " "
                + Parent.tutor_lastname_father
                + " "
                + Parent.tutor_lastname_mother
            ).label("tutor_full_name"),
            User.email.label("tutor_email"),
            (
                Parent.contact_name
                + " "
                + Parent.contact_lastname_father
                + " "
                + Parent.contact_lastname_mother
            ).label("second_tutor_full_name"),
            Parent.contact_email.label("second_tutor_email"),
        )
        .join(Camper, CamperInCamp.camper_id == Camper.id)
        .join(Parent, Camper.parent_id == Parent.id)
        .join(CamperRecord, Camper.record_id == CamperRecord.id)
        .join(User, Parent.user_id == User.id)
        .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36))
        .all()
    )
    return db_mapping_rows_to_dict(campers)


def get_campers_for_bracelets(db, camp_id):
    list_campers = (
        db.query(
            Camper.id.label("camper_id"),
            (
                Camper.name
                + " "
                + Camper.lastname_father
                + " "
                + Camper.lastname_mother
            ).label("name"),
            School.name.label("school"),
            Constant.value.label("blood_type"),
            Camper.drug_allergies.label("alergies"),
            Camper.other_allergies.label("other_alergies"),
            Camper.prohibited_foods.label("prohibed_foo"),
        )
        .select_from(CamperInCamp)
        .join(Camper, Camper.id == CamperInCamp.camper_id)
        .join(School, School.id == Camper.school_id)
        .join(Constant, Constant.id == Camper.blood_type)
        .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == 36))
        .all()
    )
    return db_mapping_rows_to_dict(list_campers)


def subscribe_camper_to_camps(db, camps_id: list[int], camper_id: int):
    extra_charges = []
    extra_questions = []

    for camp_id in camps_id:
        camper_in_camp = (
            db.query(CamperInCamp)
            .filter(
                and_(
                    CamperInCamp.camp_id == camp_id, CamperInCamp.camper_id == camper_id
                )
            )
            .first()
        )
        camp = db.query(Camp).filter(Camp.id == camp_id).first()

        camp_extra_charges = (
            db.query(
                Camp.id.label("camp_id"),
                Camp.name.label("camp_name"),
                CampExtraCharge.id.label("camp_extra_charge_id"),
                CampExtraCharge.name.label("camp_extra_charge_name"),
                CampExtraCharge.price.label("camp_extra_charge_price"),
                CamperExtraCharge.id.label("camper_extra_charge_id"),
                CamperExtraCharge.is_selected.label("camp_extra_charge_is_selected"),
            )
            .outerjoin(
                CamperExtraCharge,
                CamperExtraCharge.extra_charge_id == CampExtraCharge.id,
            )
            .join(Camp, Camp.id == CampExtraCharge.camp_id)
            .filter(CampExtraCharge.camp_id == camp_id)
            .all()
        )
        for camp_extra_charge in db_mapping_rows_to_dict(camp_extra_charges):
            extra_charges.append(camp_extra_charge)

        camp_extra_questions = (
            db.query(
                Camp.id.label("camp_id"),
                Camp.name.label("camp_name"),
                CampExtraQuestion.id.label("camp_extra_question_id"),
                CampExtraQuestion.question.label("camp_extra_question_question"),
                CampExtraQuestion.is_required.label("camp_extra_question_required") ,
                CamperExtraAnswer.id.label("camper_extra_answer_id"),
                CamperExtraAnswer.answer.label("camp_extra_answer_answer"),
            )
            .outerjoin(
                CamperExtraAnswer,
                CamperExtraAnswer.question_id == CampExtraQuestion.id,
            )
            .join(Camp, Camp.id == CampExtraQuestion.camp_id)
            .filter(CampExtraQuestion.camp_id == camp_id)
            .all()
        )
        for camp_extra_question in db_mapping_rows_to_dict(camp_extra_questions):
            extra_questions.append(camp_extra_question)

        if camper_in_camp and getattr(camper_in_camp, "status") != 36:
            db.query(CamperInCamp).filter(
                and_(
                    CamperInCamp.camp_id == camp_id, CamperInCamp.camper_id == camper_id
                )
            ).update({"status": 36})
            db.commit()
        elif not camper_in_camp:
            new_camper_in_camp = CamperInCampCreate(
                camper_id=camper_id,
                camp_id=camp_id,
                status=36,
                payment_balance=getattr(camp, "public_price"),
            )
            create_new_camper_in_camp(db, new_camper_in_camp)

    if extra_charges or extra_questions:
        return {
            "status": 2,
            "extra_charges": extra_charges,
            "extra_questions": extra_questions,
        }
    else:
        return {"status": 1}
    
