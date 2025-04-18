from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import func, desc, asc
from sqlalchemy.orm import Session, aliased
from model.catalogs.constant import Constant
from sqlalchemy import or_
from fastapi import HTTPException
from utils.db import db_mapping_rows_to_dict

from model.campers import Camper, School, CamperRecord, Parent
from model.user import User
from model.catalogs import (
    Vaccine,
    FoodRestriction,
    LicensedMedicine,
    PathologicalBackground,
    PathologicalBackgroundFamily,
)
from model.campers import (
    CamperVaccine,
    CamperLicensedMedicine,
    CamperFoodRestriction,
    CamperPathologicalBackground,
    CamperPathologicalBackgroundFamily,
)
from model.payments import CamperExtraCharge
from model.camps import CampExtraCharge

from schema.campers_catalogs.camper_food_restriction_schema import (
    CamperFoodRestrictionCreate,
    CamperFoodRestrictionModify
    )

from schema.campers_catalogs.camper_licensed_medicine_schema import (
    CamperLicensedMedicineCreate,
    CamperLicensedMedicineModify,
)
from schema.campers_catalogs.camper_vaccine_schema import (
    CamperVaccineCreate,
    CamperVaccineModify,
)
from crud.campers_catalogs.camper_vaccine_crud import (
    create_new_camper_vaccine,
    update_camper_vaccine_by_ids,
)
from crud.campers_catalogs.camper_food_restriction_crud import (
    create_new_camper_food_restriction,
    update_camper_food_restriction_by_ids,
)
from crud.campers_catalogs.camper_licensed_medicine_crud import (
    create_new_camper_licensed_medicine,
    update_camper_licensed_medicine_by_ids,
)

from schema.campers_catalogs.camper_pathological_background_schema import (
    CamperPathologicalBackCreate,
    CamperPathologicalBackModify,
)

from crud.campers_catalogs.camper_pathological_background_crud import (
    create_new_camper_pathological_background,
    update_camper_pathological_background_by_ids,
)

from schema.campers_catalogs.camper_pathological_background_fm_schema import (
    CamperPathologicalBackFmCreate,
    CamperPathologicalBackFmModify,
)
from crud.campers_catalogs.camper_pathological_background_fm_crud import (
    create_new_camper_pathological_background_fm,
    update_camper_pathological_background_fm_by_ids,
)

from schema.campers.camper_schema import CamperCreate, CamperModify, CamperComplete
from schema.campers.camper_record_schema import CamperRecordCreate
from schema.pagination.pagination_schema import SortEnum
from crud.campers.camper_record_crud import create_new_camper_record
from helper.pagination_helpers import get_number_of_pages


def get_all_camper(db: Session) -> any:
    rows = db.query(Camper).all()
    return rows


def get_camper_by_uuid(db: Session, camper_id: int) -> any:
    return db.query(Camper).filter_by(id=camper_id).first()


def create_new_camper(db: Session, camper_complete: CamperCreate) -> any:

    db_camper = None
    try:
        new_camper_record = CamperRecordCreate(attend=0, attended=0, total=0)
        camper_record = create_new_camper_record(db, new_camper_record)

        if camper_record == None:
            raise HTTPException(status_code=500, detail="Ocurrio un error al almacenar el record del camper. El camper no se creo")

        new_camper = camper_complete.camper
        new_camper = new_camper.dict()
        new_camper["record_id"] = camper_record.id
        db_camper = Camper(**new_camper)
        db.add(db_camper)
        db.commit()        
        db.refresh(db_camper)
        
    except Exception as e:
        db.rollback()
        print(e)   
        raise HTTPException(status_code=500, detail="Ocurrio un error al almacenar el camper")
    
    try:
        if len(camper_complete.vaccines) > 0:
            for vaccine in camper_complete.vaccines:
                camper_vaccine = CamperVaccineCreate(
                    camper_id=db_camper.id, vaccine_id=vaccine.id, is_active=vaccine.is_active
                )
         
                create_new_camper_vaccine(db, camper_vaccine)
                # db.add(camper_vaccine)                

        if len(camper_complete.food_restrictions) > 0:
            for food_restriction in camper_complete.food_restrictions:
                camper_food_restriction = CamperFoodRestrictionCreate(
                    camper_id=db_camper.id,
                    food_restriction_id=food_restriction.id,
                    is_active=food_restriction.is_active,
                )
                create_new_camper_food_restriction(db, camper_food_restriction)

        if len(camper_complete.licensed_medicines) > 0:
            for licensed_medicine in camper_complete.licensed_medicines:
                camper_licensed_medicine = CamperLicensedMedicineCreate(
                    camper_id=db_camper.id,
                    licensed_medicine_id=licensed_medicine.id,
                    is_active=licensed_medicine.is_active,
                )
                create_new_camper_licensed_medicine(db, camper_licensed_medicine)

        if len(camper_complete.pathological_background) > 0:
            for pathological_background in camper_complete.pathological_background:
                camper_pathological_background = CamperPathologicalBackCreate(
                    camper_id=db_camper.id,
                    pathological_background_id=pathological_background.id,
                    is_active=pathological_background.is_active,
                )
                create_new_camper_pathological_background(db, camper_pathological_background)

        if len(camper_complete.pathological_background_fm) > 0:
                for pathological_background_fm in camper_complete.pathological_background_fm:
                    camper_pathological_background_fm = CamperPathologicalBackFmCreate(
                        camper_id=db_camper.id,
                        pathological_background_fm_id=pathological_background_fm.id,
                        is_active=pathological_background_fm.is_active,
                    )
                    create_new_camper_pathological_background_fm(
                        db, camper_pathological_background_fm
                    )
    except Exception as e:
        db.delete(db_camper)
        db.commit()
        print(e)   
        raise HTTPException(status_code=500, detail="Ocurrio un error al almacenar el camper")
    return db_camper

def update_camper_by_id(
    db: Session, camper_id: int, modify_camper: CamperModify
) -> any:
    print("#################################################")
    print(type(modify_camper))
    rows_updated = (
        db.query(Camper)
        .filter_by(id=camper_id)
        .update(modify_camper, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_vaccine_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(Vaccine.id, Vaccine.name, CamperVaccine.is_active)
        .join(Camper, CamperVaccine.camper_id == Camper.id)
        .join(Vaccine, CamperVaccine.vaccine_id == Vaccine.id)
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_licensed_medicine_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            LicensedMedicine.id, LicensedMedicine.name, CamperLicensedMedicine.is_active
        )
        .join(Camper, CamperLicensedMedicine.camper_id == Camper.id)
        .join(
            LicensedMedicine,
            CamperLicensedMedicine.licensed_medicine_id == LicensedMedicine.id,
        )
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_food_restriction_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            FoodRestriction.id, FoodRestriction.name, CamperFoodRestriction.is_active
        )
        .join(Camper, CamperFoodRestriction.camper_id == Camper.id)
        .join(
            FoodRestriction,
            CamperFoodRestriction.food_restriction_id == FoodRestriction.id,
        )
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_pathological_background_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            PathologicalBackground.id,
            PathologicalBackground.name,
            CamperPathologicalBackground.is_active,
        )
        .join(Camper, CamperPathologicalBackground.camper_id == Camper.id)
        .join(
            PathologicalBackground,
            CamperPathologicalBackground.pathological_background_id
            == PathologicalBackground.id,
        )
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)

def get_camper_licensed_medicine(db: Session, camper_id: int):
    rows = (
        db.query(
            LicensedMedicine.id,
            LicensedMedicine.name,
            CamperLicensedMedicine.is_active,
        ).select_from(CamperLicensedMedicine)
        .join(LicensedMedicine, CamperLicensedMedicine.licensed_medicine_id == LicensedMedicine.id)
        .filter(CamperLicensedMedicine.camper_id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)
def get_camper_vaccines(db, camper_id):
    rows = (
        db.query(
            Vaccine.id,
            Vaccine.name,
            CamperVaccine.is_active,
        ).select_from(CamperVaccine)
        .join(Vaccine, CamperVaccine.vaccine_id == Vaccine.id)
        .filter(CamperVaccine.camper_id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)

def get_extra_charge_by_camper_camp(db, camper_id: int, camp_id: int):
    rows = (
            db.query(
                CampExtraCharge.id,
                CampExtraCharge.name,
                CampExtraCharge.price,
                CamperExtraCharge.is_selected,
            )
            .select_from(CamperExtraCharge)
            .join(
                CampExtraCharge, CampExtraCharge.id == CamperExtraCharge.extra_charge_id
            )
            .filter(
                CamperExtraCharge.camper_id == camper_id,
                CampExtraCharge.camp_id == camp_id
            ).all()
        )    
    return db_mapping_rows_to_dict(rows)

def get_pathological_background_fm_by_camper(db: Session, camper_id: int):
    rows = (
        db.query(
            PathologicalBackgroundFamily.id,
            PathologicalBackgroundFamily.name,
            CamperPathologicalBackgroundFamily.is_active,
        )
        .join(Camper, CamperPathologicalBackgroundFamily.camper_id == Camper.id)
        .join(
            PathologicalBackgroundFamily,
            CamperPathologicalBackgroundFamily.pathological_background_family_id
            == PathologicalBackgroundFamily.id,
        )
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(rows)


def get_campers_from_parent(db: Session, parent_id: int):
    rows = (
        db.query(
            Camper.id,
            Camper.photo,
            (
                Camper.name
                + " "
                + Camper.lastname_father
                + " "
                + Camper.lastname_mother
            ).label("full_name"),
            School.name.label("school"),
        )
        .join(School, School.id == Camper.school_id)
        .filter(Camper.parent_id == parent_id)
        .all()
    )

    return db_mapping_rows_to_dict(rows)


def get_camper_band(db: Session, camper_id):
    camper = (
        db.query(
            (
                Camper.name
                + " "
                + Camper.lastname_father
                + " "
                + Camper.lastname_mother
            ).label("full_name"),
            School.name.label("school"),
            Camper.photo.label("photo"),
            Camper.birthday.label("birthday"),
            CamperRecord.attend.label("future_camps"),
            CamperRecord.attended.label("past_camps"),
        )
        .join(School, School.id == Camper.school_id)
        .join(CamperRecord, CamperRecord.id == Camper.record_id)
        .filter(Camper.id == camper_id)
        .all()
    )
    return db_mapping_rows_to_dict(camper)


def delete_camper(db, camper_id: int):
    camper = db.query(Camper).filter(Camper.id == camper_id).first()
    if camper == None:
        return None
    try:
        db.delete([])
        db.commit()
        
    except IntegrityError:
        db.rollback()
        return {"status": 2, "msg": "Can not delete camper, referenced by other table"}
    except:
        db.rollback()
        return {"status": 3, "msg": "Internal Server Error"}
    return {"status" : 1, "msg": "Camper deleted successfully"}


def search_camper_by_name_user(db: Session, search: str):
    campers = (
        db.query(
            Camper.id.label("camper_id"),
            Camper.name.label("camper_name"),
            Camper.lastname_father.label("camper_lastname_father"),
            Camper.lastname_mother.label("camper_lastname_mother"),
            School.name.label("school"),
            Camper.updated_at.label("updated"),
            Parent.id.label("tutor_id"),
            (
                Parent.tutor_name
                + " "
                + Parent.tutor_lastname_father
                + " "
                + Parent.tutor_lastname_mother
            ).label("tutor_fullname"),
            User.id.label("user_id"),
            User.email.label("tutor_email"),
        )
        .join(Parent, Parent.id == Camper.parent_id)
        .join(User, User.id == Parent.user_id)
        .join(School, School.id == Camper.school_id)
        .filter(
            or_(
                Camper.name.ilike(r"%{}%".format(search)),
                Camper.lastname_father.ilike(r"%{}%".format(search)),
                Camper.lastname_mother.ilike(r"%{}%".format(search)),
                School.name.ilike(r"%{}%".format(search)),
                Parent.tutor_name.ilike(r"%{}%".format(search)),
                Parent.tutor_lastname_father.ilike(r"%{}%".format(search)),
                Parent.tutor_lastname_mother.ilike(r"%{}%".format(search)),
                User.email.ilike(r"%{}%".format(search)),
            )
        )
        .all()
    )
    if campers:
        return db_mapping_rows_to_dict(campers)
    else:
        return "Data not found"



def get_all_camper_admin(db: Session, pagination):
    order = desc if pagination.order == SortEnum.DESC else asc
    query = (
        db.query(
            Camper.id.label("camper_id"),
            Camper.name.label("camper_name"),
            Camper.lastname_father.label("camper_lastname_father"),
            Camper.lastname_mother.label("camper_lastname_mother"),
            School.name.label("school"),
            Camper.updated_at.label("updated"),
            Parent.id.label("tutor_id"),
            (
                Parent.tutor_name
                + " "
                + Parent.tutor_lastname_father
                + " "
                + Parent.tutor_lastname_mother
            ).label("tutor_fullname"),
            User.id.label("user_id"),
            User.email.label("tutor_email"),
        )
        .join(Parent, Parent.id == Camper.parent_id)
        .join(User, User.id == Parent.user_id)
        .join(School, School.id == Camper.school_id)
        .order_by(order(Camper.name))
        .limit(pagination.perPage)
        .offset((pagination.offset))
    )
    data = db.execute(query)
    data = data.mappings().all()
    rows_count = db.query(func.count(Camper.id)).select_from(Camper).join(Parent, Parent.id == Camper.parent_id).join(User, User.id == Parent.user_id).join(School, School.id == Camper.school_id).scalar()    
    pages = get_number_of_pages(rows_count, pagination.perPage)

    return {
        "pages": pages,
        "items": data,
        "total": rows_count,
    }

def search_all_camper_admin(db: Session, pagination, camper_name: str, camper_lastname_father: str , camper_lastname_mother: str, tutor_1_name: str, tutor_1_lastname_father: str, tutor_1_lastname_mother: str, tutor_1_email: str, tutor_2_name: str, tutor_2_lastname_father: str,tutor_2_lastname_mother: str, tutor_2_email: str):
    query = (
        db.query(
            Camper.id.label("camper_id"),
            Camper.name.label("camper_name"),
            Camper.lastname_father.label("camper_lastname_father"),
            Camper.lastname_mother.label("camper_lastname_mother"),
            School.name.label("school"),
            Camper.updated_at.label("updated"),
            Parent.id.label("tutor_id"),
            (
                Parent.tutor_name
                + " "
                + Parent.tutor_lastname_father
                + " "
                + Parent.tutor_lastname_mother
            ).label("tutor_fullname"),
            User.id.label("user_id"),
            User.email.label("tutor_email"),
        )
        .join(Parent, Parent.id == Camper.parent_id)
        .join(User, User.id == Parent.user_id)
        .join(School, School.id == Camper.school_id)
        .filter(
            or_(
                Camper.name.op('%')(camper_name),
                Camper.lastname_father.op('%')(camper_lastname_father),
                Camper.lastname_mother.op('%')(camper_lastname_mother),
                User.email.op('%')(tutor_1_email),
                Parent.tutor_name.op('%')(tutor_1_name),
                Parent.tutor_lastname_father.op('%')(tutor_1_lastname_father),
                Parent.tutor_lastname_mother.op('%')(tutor_1_lastname_mother),
                Parent.contact_name.op('%')(tutor_2_name),
                Parent.contact_lastname_father.op('%')(tutor_2_lastname_father),
                Parent.contact_lastname_mother.op('%')(tutor_2_lastname_mother),
                Parent.contact_email.op('%')(tutor_2_email),
            ) 
        )
        .order_by(
            func.similarity(Camper.name, camper_name).desc(),
            func.similarity(Camper.lastname_father, camper_lastname_father).desc(),
            func.similarity(Camper.lastname_mother, camper_lastname_mother).desc(),
            func.similarity(User.email, tutor_1_email).desc(),
            func.similarity(Parent.tutor_name, tutor_1_name).desc(),
            func.similarity(Parent.tutor_lastname_father, tutor_1_lastname_father).desc(),
            func.similarity(Parent.tutor_lastname_mother, tutor_1_lastname_mother).desc(),
            func.similarity(Parent.contact_name, tutor_2_name).desc(),
            func.similarity(Parent.contact_lastname_father, tutor_2_lastname_father).desc(),
            func.similarity(Parent.contact_lastname_mother, tutor_2_lastname_mother).desc(),
            func.similarity(Parent.contact_email, tutor_2_email).desc(),
        )
        .limit(pagination.perPage)
        .offset((pagination.offset))
    )
    print(query)
    data = db.execute(query)
    data = data.mappings().all()
    rows_count = (db.query(func.count(Camper.id)).select_from(Camper).join(Parent, Parent.id == Camper.parent_id).join(User, User.id == Parent.user_id).join(School, School.id == Camper.school_id)        .filter(
            or_(
                Camper.name.op('%')(camper_name),
                Camper.lastname_father.op('%')(camper_lastname_father),
                Camper.lastname_mother.op('%')(camper_lastname_mother),
                User.email.op('%')(tutor_1_email),
                Parent.tutor_name.op('%')(tutor_1_name),
                Parent.tutor_lastname_father.op('%')(tutor_1_lastname_father),
                Parent.tutor_lastname_mother.op('%')(tutor_1_lastname_mother),
                Parent.contact_name.op('%')(tutor_2_name),
                Parent.contact_lastname_father.op('%')(tutor_2_lastname_father),
                Parent.contact_lastname_mother.op('%')(tutor_2_lastname_mother),
                Parent.contact_email.op('%')(tutor_2_email),
            ) 
        ).scalar())    
    pages = get_number_of_pages(rows_count, pagination.perPage)

    return {
        "pages": pages,
        "items": data,
        "total": rows_count,
    }

def get_campers_in_school(db: Session, school_id:str):
    query = db.query(func.concat(Camper.name, " ", Camper.lastname_father, " ", Camper.lastname_mother).label("fullname")).filter(Camper.school_id == school_id)
    data = db.execute(query)
    data = data.mappings().all()
    return data