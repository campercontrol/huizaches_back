from xmlrpc.client import boolean

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from crud.camps.camp_crud import (
    get_all_camp,
    get_all_active_camp,
    get_school_camp_for_camper,
    get_camp_by_id,
    create_new_camp,
    update_camp_by_id,
    delete_camp,
    get_camp_by_search,
    create_new_camp_payment_account  
)
from crud.campers.camper_crud import get_camper_by_uuid
from crud.campers.camper_extra_answer_crud import update_extra_answer_by_id
from crud.catalogs.payment_account_crud import  get_payment_account_for_camp
from schema.campers.camper_extra_answer_schema import CamperExtraAnswerModify, UpdateCamperExtraAnswer

from crud.camps.camper_in_camp_crud import (
    create_new_camper_in_camp,
    get_all_camper_in_camp,
    update_camper_extra_charges,
    get_camper_in_camp_by_camper_camp,
    update_camper_in_camp_by_id,
    get_campers_for_camp,
    subscribe_camper_to_camps,
    create_update_camper_extras_camp,
    get_campers_in_camp_and_groupings
)

from crud.camps.camp_extra_charge_crud import (
    get_extra_charge_by_camp,
    create_new_extra_charge,
)
from crud.camps.camp_extra_question_crud import (
    get_extra_question_by_camp,
    create_new_extra_question,
)
from crud.camps.camp_discount_crud import get_camp_discount_by_camp
from crud.camps.staff_in_camp_crud import get_staff_volunteer_in_camp, get_staff_in_camp
from crud.camps.location_crud import get_location_by_uuid
from schema.camps.camp_schema import CampComplete
from schema.camps.camper_in_camp_schema import CamperInCampCreate, CamperInCampModify
from schema.camps.camp_payment_account_schema import CreateCampPaymentAccount
from schema.payments.payment_schema import PaymentCreate
from schema.camps.camp_extra_charge_schema import CampExtraChargeCreate
from schema.camps.camp_extra_question_schema import CampExtraQuestionCreate
from schema.campers.camper_extra_answer_schema import ExtraAnswerMultiple
from schema.payments.camper_extra_charge_schema import ExtraChargeMultiple

from utils.db import SessionLocal

camp_router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@camp_router.get("/camp/", tags=["Camps"])
def get_camp(db: Session = Depends(get_db)):
    list_camp = get_all_camp(db)
    return {"data": list_camp}


@camp_router.get("/active_camp/", tags=["Camps"])
def get__active_camp(db: Session = Depends(get_db)):
    list_camp = get_all_active_camp(db)
    return {"data": list_camp}


@camp_router.get("/get_camps_for_camper/{camper_id}", tags=["Camps"])
def get_camps_for_camper(camper_id: int, db: Session = Depends(get_db)):
    list_camp = get_school_camp_for_camper(db, camper_id)
    return {"data": list_camp}


@camp_router.get("/camp/{camp_id}", tags=["Camps"])
def get_camp_id(camp_id: int, db: Session = Depends(get_db)):
    camp = get_camp_by_id(db, camp_id)
    extra_charges = get_extra_charge_by_camp(db, camp_id)
    extra_questions = get_extra_question_by_camp(db, camp_id)
    extra_discounts = get_camp_discount_by_camp(db, camp_id)
    payment_accounts = get_payment_account_for_camp(db, camp_id)

    return {
        "camp": camp,
        "payment_accounts": payment_accounts,
        "extra_charges": extra_charges,
        "extra_questions": extra_questions,
        "extra_discounts": extra_discounts,
    }


@camp_router.post("/camp/", tags=["Camps"])
def create_camp(new_camp: CampComplete, db: Session = Depends(get_db)):
    camp = create_new_camp(db, new_camp.camp)
    new_camp_id = getattr(camp, "id")
    payment_accounts = new_camp.payment_accounts
    if payment_accounts:
        for payment_account in payment_accounts:
            new_camp_payment_account_obj = CreateCampPaymentAccount(
                camp_id= new_camp_id,
                paymentaccount_id = payment_account.id
            )
            create_new_camp_payment_account(db, new_camp_payment_account_obj)
        
    if new_camp.extra_question:
        for question in new_camp.extra_question:
            new_question = CampExtraQuestionCreate(
                question=question.question,
                is_required=question.is_required,
                camp_id=new_camp_id,
            )
            create_new_extra_question(db, new_question)

    if new_camp.extra_charges:
        for charge in new_camp.extra_charges:
            new_charge = CampExtraChargeCreate(
                name=charge.name,
                price=charge.price,
                currency_id=charge.currency_id,
                camp_id=new_camp_id,
            )
            create_new_extra_charge(db, new_charge)

    return {"data": camp}


@camp_router.patch("/camp/{camp_id}", tags=["Camps"])
def update_camp(camp_id: int, modify_camp: CampComplete, db: Session = Depends(get_db)):
    update_data = modify_camp.camp.dict(exclude_unset=True)
    camp_update_result = update_camp_by_id(db, camp_id, update_data)

    if camp_update_result != 0:
        exist_camp = get_camp_by_id(db, camp_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_camp}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}


@camp_router.post("/subscribe_camp/", tags=["Camps"])
def subscribe_camp(
    new_camper_in_camp: CamperInCampCreate, db: Session = Depends(get_db)
):
    camper_in_camp = create_new_camper_in_camp(db, new_camper_in_camp)
    camp = get_camp_by_id(db, new_camper_in_camp.camp_id)
    camper = get_camper_by_uuid(db, new_camper_in_camp.camper_id)

    payment = PaymentCreate(
        paid=False,
        payment_amount=new_camper_in_camp.payment_balance,
        payment_date=date.today(),
        txn_number="Cargo por campamento",
        camp_id=new_camper_in_camp.camp_id,
        camper_id=new_camper_in_camp.camper_id,
        currency_id=camp.currency_id,
        parent_id=camper.parent_id,
        payment_method_id=3,
        txn_type_id=2,
    )
    return {"camper_in_camp": camper_in_camp, "payment": payment}


@camp_router.post("/unsubscribe_camp/", tags=["Camps"])
def unsubscribe_camp(camp_id: int, camper_id: int, db: Session = Depends(get_db)):
    camper_in_camp = get_camper_in_camp_by_camper_camp(db, camper_id, camp_id)
    new_camper_in_camp = CamperInCampModify(
        status=37,
        payment_balance=camper_in_camp.payment_balance,
        camp_id=camp_id,
        camper_id=camper_id,
    ).dict(exclude_unset=True)
    modify_camper_in_camp = update_camper_in_camp_by_id(
        db, camp_id, camper_id, new_camper_in_camp
    )
    return modify_camper_in_camp


@camp_router.get("/camperincamp/", tags=["Camps"])
def get_camperincamp(db: Session = Depends(get_db)):
    list_camp = get_all_camper_in_camp(db)
    return {"data": list_camp}


@camp_router.get("/camp_extras/{camp_id}", tags=["Camps"])
def get_camp_extras(camp_id: int, db: Session = Depends(get_db)):
    extra_charges = get_extra_charge_by_camp(db, camp_id)
    extra_questions = get_extra_question_by_camp(db, camp_id)
    data = {"extra_charges": extra_charges, "extra_questions": extra_questions}
    return data


@camp_router.delete("/delete_camp/{camp_id}", tags=["Camps"])
def delete_camp_by_id(camp_id: int, db: Session = Depends(get_db)):
    status = delete_camp(db, camp_id)
    return {"status": status}


@camp_router.get("/staff/camp/{camp_id}", tags=["Camps"])
def get_staff_camp(camp_id: int, db: Session = Depends(get_db)):
    camp_info = get_camp_by_id(db, camp_id)
    campers = get_campers_for_camp(db, camp_id)
    staff_volunteer = get_staff_volunteer_in_camp(db, camp_id)
    staff = get_staff_in_camp(db, camp_id)
    location = get_location_by_uuid(db, camp_info.location_id)
    return {
        "camp": camp_info,
        "location": location.name,
        "campers": campers,
        "staff_volunteer": staff_volunteer,
        "staff_confirmed": staff,
    }


@camp_router.post("/camper/subscribe/camps/", tags=["Camps"])
def subscrible_camper_to_multiple_camps(
    camps_id: list[int], camper_id: int, db: Session = Depends(get_db)
):
    data = subscribe_camper_to_camps(db, camps_id, camper_id)
    if data["status"] == 1:
        return {"status": data["status"], "prev_camps": data["prev_camps"]}
    else:
        return {
            "status": data["status"],
            "prev_camps": data["prev_camps"],
            "extra_charges": data["extra_charges"],
            "extra_questions": data["extra_questions"],
        }


@camp_router.post("/camper/extras/camp/", tags=["Camps"])
def post_extras_camp_for_camper(
    camper_id: int,
    extra_answers: list[ExtraAnswerMultiple],
    extra_charges: list[ExtraChargeMultiple],
    db: Session = Depends(get_db),
):
    status = create_update_camper_extras_camp(
        db, camper_id, extra_answers, extra_charges
    )
    return {"status": status}

@camp_router.patch("/camper/extra_charges/", tags=["Camps"])
def post_extras_camp_for_camper(
    camper_id: int,
    extra_charges: "list[ExtraChargeMultiple]",
    db: Session = Depends(get_db),
):
    result = update_camper_extra_charges(
        db, camper_id, extra_charges
    )
    if result == 1:
        return {"detail": {"status": 1, "msg": "Camper extra charges updated succesfully"}}
    if result == 3:
        raise HTTPException(status_code=500, detail= {"status": 3, "msg": "An unknown error ocurred while updating"})


@camp_router.patch("/camper/extra_answers/", tags=["Camps"])
def update_extra_answers_for_camper(
    extra_answers: "list[UpdateCamperExtraAnswer]",
    db: Session = Depends(get_db),
):   
    response = update_extra_answer_by_id(
        db, extra_answers
    )
    if response == None:
        raise HTTPException(status_code=500, detail= {"status": 3, "msg": "An error ocurred while saving"})
    if response == 1:
        return {"detail": {"status": 1, "msg": "Extra answers updated succesfully"}}
    if response == 0:
        return {"detail": {"status": 2, "msg": "Extra answers not found"}}
        
        

@camp_router.get("/search/camp/{search}", tags=["Camps"])
def get_search_camp(search: str, db: Session = Depends(get_db)):
    possible_camps = get_camp_by_search(db, search)
    return {"data": possible_camps}

@camp_router.get("/camps/{camp_id}/groupings/campers", tags=["GroupingCamp"])
def get_campers_in_camp_and_groupings_endpoint(camp_id: int, db: Session = Depends(get_db)):
    campers_groupings = get_campers_in_camp_and_groupings(db,camp_id)

    if len(campers_groupings) == 0:
        raise HTTPException(status_code=404, detail="Camp not found")
    return {"data": campers_groupings}