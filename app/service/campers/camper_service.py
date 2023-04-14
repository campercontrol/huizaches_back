from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session, add_mapped_attribute
from typing import List

from crud.catalogs.constant_crud import (
    get_all_blood_type_id_name,
    get_all_gender_id_name,
    get_all_grade_id_name,
)
from crud.catalogs.vaccine_crud import get_all_vaccine_id_name
from crud.campers_catalogs.camper_vaccine_crud import (
    create_new_camper_vaccine,
    update_camper_vaccine_by_ids,
)
from crud.catalogs.food_restriction_crud import get_all_food_restriction_id_name
from crud.catalogs.licensed_medicine_crud import get_all_licensed_medicine_id_name
from crud.catalogs.pathological_background_crud import (
    get_all_pathological_background_id_name,
)
from crud.catalogs.pathological_background_family_crud import (
    get_all_pathological_background_family_id_name,
)
from crud.campers_catalogs.camper_food_restriction_crud import (
    create_new_camper_food_restriction,
    update_camper_food_restriction_by_ids,
)
from crud.campers_catalogs.camper_licensed_medicine_crud import (
    create_new_camper_licensed_medicine,
    update_camper_licensed_medicine_by_ids,
)
from crud.campers_catalogs.camper_pathological_background_crud import (
    create_new_camper_pathological_background,
    update_camper_pathological_background_by_ids,
)
from crud.campers_catalogs.camper_pathological_background_fm_crud import (
    create_new_camper_pathological_background_fm,
    update_camper_pathological_background_fm_by_ids,
)
from crud.campers.camper_crud import (
    get_all_camper,
    get_camper_by_uuid,
    create_new_camper,
    update_camper_by_id,
    get_vaccine_by_camper,
    get_licensed_medicine_by_camper,
    get_food_restriction_by_camper,
    get_pathological_background_by_camper,
    get_pathological_background_fm_by_camper,
    get_campers_from_parent
)
from crud.campers.school_crud import get_active_school
from schema.campers_catalogs.camper_vaccine_schema import (
    CamperVaccineCreate,
    CamperVaccineModify,
)
from schema.campers_catalogs.camper_food_restriction_schema import (
    CamperFoodRestrictionCreate,
    CamperFoodRestrictionModify,
)
from schema.campers_catalogs.camper_licensed_medicine_schema import (
    CamperLicensedMedicineCreate,
    CamperLicensedMedicineModify,
)
from schema.campers_catalogs.camper_pathological_background_schema import (
    CamperPathologicalBackCreate,
    CamperPathologicalBackModify,
)
from schema.campers_catalogs.camper_pathological_background_fm_schema import (
    CamperPathologicalBackFmCreate,
    CamperPathologicalBackFmModify,
)

from schema.campers.camper_schema import CamperCreate, CamperModify, CamperComplete
from utils.db import SessionLocal

from utils.db import db_mapping_rows_to_dict

camper_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@camper_routes.get("/camper/", tags=["Campers"])
def get_camper(db: Session = Depends(get_db)):
    list_camper = get_all_camper(db)
    return {"data": list_camper}


@camper_routes.get("/camper/{camper_id}", tags=["Campers"])
def get_camper_by_id(camper_id: str, db: Session = Depends(get_db)):
    list_camper = get_camper_by_uuid(db, camper_id)
    return {"data": list_camper}


@camper_routes.get("/camper_complete/{camper_id}/{language}", tags=["Campers"])
def get_camper_by_id_complete(
    camper_id: str, language: str, db: Session = Depends(get_db)
):
    genders = get_all_gender_id_name(db, language)
    blood_type = get_all_blood_type_id_name(db, language)
    schools = (get_active_school(db),)
    grades = get_all_grade_id_name(db, language)
    list_camper = get_camper_by_uuid(db, camper_id)
    vaccines = get_vaccine_by_camper(db, camper_id)
    licensed_medicines = get_licensed_medicine_by_camper(db, camper_id)
    food_restrictions = get_food_restriction_by_camper(db, camper_id)
    pathological_backgrounds = get_pathological_background_by_camper(db, camper_id)
    pathological_backgrounds_family = get_pathological_background_fm_by_camper(
        db, camper_id
    )
    data = {
        "camper": list_camper,
        "vaccines": vaccines,
        "licensed_medicines": licensed_medicines,
        "food_restrictions": food_restrictions,
        "pathological_background": pathological_backgrounds,
        "pathological_background_fm": pathological_backgrounds_family,
        "genders": genders,
        "blood_types": blood_type,
        "school": schools,
        "grades": grades,
    }
    return data


@camper_routes.post("/camper/", tags=["Campercamper_schema"])
def create_camper(camper_complete: CamperComplete, db: Session = Depends(get_db)):
    new_camper = create_new_camper(db, camper_complete.camper)
    new_camper_id = getattr(new_camper, "id")

    for vaccine in camper_complete.vaccines:
        camper_vaccine = CamperVaccineCreate(
            camper_id=new_camper_id, vaccine_id=vaccine.id, is_active=vaccine.is_active
        )
        print(camper_vaccine)
        create_new_camper_vaccine(db, camper_vaccine)

    for food_restriction in camper_complete.food_restrictions:
        camper_food_restriction = CamperFoodRestrictionCreate(
            camper_id=new_camper_id,
            food_restriction_id=food_restriction.id,
            is_active=food_restriction.is_active,
        )
        create_new_camper_food_restriction(db, camper_food_restriction)

    for licensed_medicine in camper_complete.licensed_medicines:
        camper_licensed_medicine = CamperLicensedMedicineCreate(
            camper_id=new_camper_id,
            licensed_medicine_id=licensed_medicine.id,
            is_active=licensed_medicine.is_active,
        )
        create_new_camper_licensed_medicine(db, camper_licensed_medicine)

    for pathological_background in camper_complete.pathological_background:
        camper_pathological_background = CamperPathologicalBackCreate(
            camper_id=new_camper_id,
            pathological_background_id=pathological_background.id,
            is_active=pathological_background.is_active,
        )
        create_new_camper_pathological_background(db, camper_pathological_background)

    for pathological_background_fm in camper_complete.pathological_background_fm:
        camper_pathological_background_fm = CamperPathologicalBackFmCreate(
            camper_id=new_camper_id,
            pathological_background_fm_id=pathological_background_fm.id,
            is_active=pathological_background_fm.is_active,
        )
        create_new_camper_pathological_background_fm(
            db, camper_pathological_background_fm
        )

    return camper_complete


@camper_routes.patch("/camper/{camper_id}", tags=["Campers"])
def update_camper(
    camper_id: int, modify_camper: CamperComplete, db: Session = Depends(get_db)
):
    update_data = modify_camper.dict(exclude_unset=True)
    print(update_data)
    camper_upcdate_result = update_camper_by_id(db, camper_id, update_data["camper"])

    for vaccine in update_data["vaccines"]:
        camper_vaccine = CamperVaccineModify(
            camper_id=camper_id,
            vaccine_id=vaccine["id"],
            is_active=vaccine["is_active"],
        ).dict(exclude_unset=True)
        update_camper_vaccine_by_ids(db, vaccine["id"], camper_id, camper_vaccine)

    for food_restriction in update_data["food_restrictions"]:
        camper_food_restriction = CamperFoodRestrictionModify(
            camper_id=camper_id,
            food_restriction_id=food_restriction["id"],
            is_active=food_restriction["is_active"],
        ).dict(exclude_unset=True)
        update_camper_food_restriction_by_ids(
            db, food_restriction["id"], camper_id, camper_food_restriction
        )

    for licensed_medicine in update_data["licensed_medicines"]:
        camper_licensed_medicine = CamperLicensedMedicineModify(
            camper_id=camper_id,
            licensed_medicine_id=licensed_medicine["id"],
            is_active=licensed_medicine["is_active"],
        ).dict(exclude_unset=True)
        update_camper_licensed_medicine_by_ids(
            db, licensed_medicine["id"], camper_id, camper_licensed_medicine
        )

    for pathological_back in update_data["pathological_background"]:
        camper_pathological_back = CamperPathologicalBackModify(
            camper_id=camper_id,
            pathological_background_id=pathological_back["id"],
            is_active=pathological_back["is_active"],
        ).dict(exclude_unset=True)
        update_camper_pathological_background_by_ids(
            db, pathological_back["id"], camper_id, camper_pathological_back
        )

    for pathological_back_fm in update_data["pathological_background_fm"]:
        camper_pathological_back = CamperPathologicalBackFmModify(
            camper_id=camper_id,
            pathological_background_family_id=pathological_back_fm["id"],
            is_active=pathological_back_fm["is_active"],
        ).dict(exclude_unset=True)
        update_camper_pathological_background_fm_by_ids(
            db, pathological_back_fm["id"], camper_id, camper_pathological_back
        )

    if camper_upcdate_result != 0:
        exist_camper = get_camper_by_uuid(db, camper_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_camper}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}


@camper_routes.get("/camper/{camper_id}/vaccines/")
def get_vaccine_by_camper_id(camper_id: int, db: Session = Depends(get_db)):
    list_vaccine = get_vaccine_by_camper(db, camper_id)
    return {"data": list_vaccine}


@camper_routes.get("/camper_form/{language}")
def get_camperform(language: str, db: Session = Depends(get_db)):
    genders = get_all_gender_id_name(db, language)
    blood_type = get_all_blood_type_id_name(db, language)
    schools = get_active_school(db)
    grades = get_all_grade_id_name(db, language)
    vaccines = get_all_vaccine_id_name(db)
    for x in range(0, len(vaccines)):
        vaccines[x] = dict(vaccines[x])
        vaccines[x]["is_active"] = False

    licensed_medicines = get_all_licensed_medicine_id_name(db)
    for x in range(0, len(licensed_medicines)):
        licensed_medicines[x] = dict(licensed_medicines[x])
        licensed_medicines[x]["is_active"] = False

    food_restrictions = get_all_food_restriction_id_name(db)
    for x in range(0, len(food_restrictions)):
        food_restrictions[x] = dict(food_restrictions[x])
        food_restrictions[x]["is_active"] = False

    pathological_backgrounds = get_all_pathological_background_id_name(db)
    for x in range(0, len(pathological_backgrounds)):
        pathological_backgrounds[x] = dict(pathological_backgrounds[x])
        pathological_backgrounds[x]["is_active"] = False

    pathological_backgrounds_family = get_all_pathological_background_family_id_name(db)
    for x in range(0, len(pathological_backgrounds_family)):
        pathological_backgrounds_family[x] = dict(pathological_backgrounds_family[x])
        pathological_backgrounds_family[x]["is_active"] = False

    data = {
        "camper": {
            "name": "string",
            "lastname_father": "string",
            "lastname_mother": "string",
            "photo": "string",
            "gender_id": 0,
            "birthday": "2023-04-11",
            "height": 0,
            "weight": 0,
            "grade": 0,
            "school_id": 0,
            "school_other": "string",
            "email": "string",
            "can_swim": 0,
            "affliction": "string",
            "blood_type": 0,
            "heart_problems": "string",
            "psicology_treatments": "string",
            "prevent_activities": "string",
            "drug_allergies": "string",
            "other_allergies": "string",
            "nocturnal_disorders": "string",
            "phobias": "string",
            "drugs": "string",
            "doctor_precall": True,
            "prohibited_foods": "string",
            "comments_admin": "string",
            "insurance": True,
            "insurance_company": True,
            "insurance_number": "string",
            "security_social_number": "string",
            "contact_name": "string",
            "contact_relation": "string",
            "contact_homephone": "string",
            "contact_cellphone": "string",
            "record_id": 1,
            "parent_id": 1,
        },
        "genders": genders,
        "blood_types": blood_type,
        "school": schools,
        "grades": grades,
        "vaccines": vaccines,
        "licensed_medicines": licensed_medicines,
        "food_restrictions": food_restrictions,
        "pathological_background": pathological_backgrounds,
        "pathological_background_fm": pathological_backgrounds_family,
    }
    return data

@camper_routes.get("/campers_from_parent/{parent_id}", tags=["Campers"])
def get_campers_by_parent_id(parent_id: int, db: Session = Depends(get_db)):
    list_camper = get_campers_from_parent(db, parent_id)
    return {"data": list_camper}