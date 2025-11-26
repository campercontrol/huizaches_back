import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime

from model.catalogs import Currency
from model.payments import CamperExtraCharge
from model.camps import CampExtraCharge
from model.camps.camp import Camp
from model.campers.parent import Parent
from model.campers.camper import Camper

from schema.payments.camper_extra_charge_schema import (
    CamperExtraChargeCreate,
    CamperExtraChargeModify,
    CamperExtraChargeListCreate,
)
from crud.payments.payment_crud import create_new_payment_and_update_balance_transaction, delete_payment_and_update_balance_transaction

TRANSACTION_TYPE_CAMP_ADDITIONAL_SERVICE_ID = os.getenv("TRANSACTION_TYPE_CAMP_ADDITIONAL_SERVICE_ID")

def get_all_camper_extra_charge(db):
    rows = db.query(CamperExtraCharge).all()
    return rows


def get_camper_extra_charge_by_id(db, camper_extra_charge_id: int):
    return (
        db.query(CamperExtraCharge)
        .filter_by(
            id=camper_extra_charge_id,
        )
        .first()
    )


def create_new_camper_extra_charge(
    db, new_camper_extra_charge: CamperExtraChargeCreate
):
    db_camper_extra_charge = None
    try:
        db_camper_extra_charge = CamperExtraCharge(**new_camper_extra_charge.dict())
        db.add(db_camper_extra_charge)
        db.commit()
        db.refresh(db_camper_extra_charge)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_camper_extra_charge = None
        return db_camper_extra_charge
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_camper_extra_charge



def create_new_camper_extra_charge_transaction(
    db, new_camper_extra_charge: CamperExtraChargeCreate
):

    db_camper_extra_charge = CamperExtraCharge(**new_camper_extra_charge.dict(exclude_unset=True))
    db.add(db_camper_extra_charge)
    db.flush()
    return db_camper_extra_charge



def update_camper_extra_charge_by_id(
    db, camper_extra_charge_id: int, modify_camper_extra_charge: CamperExtraChargeModify
):
    rows_updated = (
        db.query(CamperExtraCharge)
        .filter_by(id=camper_extra_charge_id)
        .update(modify_camper_extra_charge, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

def update_camper_extra_charge_by_id_and_update_balance(db: Session, camper_extra_charges):    
    try:
        for camper_extra_charge in camper_extra_charges:
            db_camper_extra_charge = db.query(CamperExtraCharge).filter(CamperExtraCharge.id == camper_extra_charge.id).first()
            db_parent = db.query(Parent.id).select_from(Parent).join(Camper, Camper.parent_id == Parent.id).filter(Camper.id == db_camper_extra_charge.camper_id).first()
            db_camp_extra_charge = db.query(CampExtraCharge).filter(CampExtraCharge.id == db_camper_extra_charge.extra_charge_id).first()
            db_camp = db.query(Camp).filter(Camp.id == db_camp_extra_charge.camp_id).first()
            if camper_extra_charge.is_selected == True:
                new_camper_extra_charge = camper_extra_charge.dict()
                if db_camper_extra_charge.payment_id is None:
                    payment_extra_charge = {
                        "paid": False,
                        "payment_amount": db_camp_extra_charge.price,
                        "txn_number": "Costo extra" + db_camp_extra_charge.name,
                        "camp_id": db_camp_extra_charge.camp_id,
                        "payment_date": datetime.now(),
                        "camper_id": db_camper_extra_charge.camper_id,
                        "currency_id": db_camp.currency_id,
                        "parent_id": db_parent.id,
                        "txn_type_id": TRANSACTION_TYPE_CAMP_ADDITIONAL_SERVICE_ID
                    }
                    db_payment_extra_charge = create_new_payment_and_update_balance_transaction(db, payment_extra_charge)                        
                    new_camper_extra_charge['payment_id'] = db_payment_extra_charge.id
                    
                db.query(CamperExtraCharge).filter_by(id=db_camper_extra_charge.id).update(new_camper_extra_charge, synchronize_session="fetch")
            
            else: 
                if db_camper_extra_charge.payment_id is not None:
                    delete_payment_and_update_balance_transaction(db, db_camper_extra_charge.payment_id, db_camper_extra_charge.camper_id)
                db.query(CamperExtraCharge).filter_by(id=db_camper_extra_charge.id).update(camper_extra_charge.dict(), synchronize_session="fetch")
                
        db.commit()        
        return 1
    except Exception as ex:
        db.rollback()
        print(ex)
        return 3 


def get_extra_charge_by_camper_camp(db, camper_id: int, camp_id: int):
    query = (
            db.query(
                CampExtraCharge.id.label("extra_charge_id"),
                CampExtraCharge.name.label("extra_charge_name"),
                Currency.symbol.label("extra_charge_symbol"),
                CampExtraCharge.price.label("extra_charge_price"),
                CamperExtraCharge.is_selected.label("extra_selected"),
                CamperExtraCharge.id.label("camper_extra_charge_id")
            )
            .select_from(CamperExtraCharge)
            .join(
                CampExtraCharge, CampExtraCharge.id == CamperExtraCharge.extra_charge_id
            ).join(
                Currency, CampExtraCharge.currency_id == Currency.id
            )
            .filter(
                CamperExtraCharge.camper_id == camper_id,
                CampExtraCharge.camp_id == camp_id
            )
        )    
    extra_charges = db.execute(query)
    extra_charges = extra_charges.mappings().all()
    return extra_charges


def create_update_extra_charges(db, extra_charges: CamperExtraChargeListCreate):
    for extra_charge in extra_charges.extra_charges:
        row = (
            db.query(CamperExtraCharge)
            .join(
                CampExtraCharge, CampExtraCharge.id == CamperExtraCharge.extra_charge_id
            )
            .filter(
                CamperExtraCharge.extra_charge_id
                == getattr(extra_charge, "extra_charge_id")
            )
            .first()
        )

        if row:
            camper_schema = CamperExtraChargeModify(
                id=getattr(row, "id"),
                is_selected=getattr(extra_charge, "extra_selected"),
                camper_id=getattr(row, "camper_id"),
                extra_charge_id=getattr(row, "extra_charge_id"),
            )
            extra_c = update_camper_extra_charge_by_id(
                db, getattr(row, "id"), camper_schema.dict()
            )
        else:
            camper_schema = CamperExtraChargeCreate(
                is_selected=getattr(extra_charge, "extra_selected"),
                camper_id=getattr(extra_charge, "camper_id"),
                extra_charge_id=getattr(extra_charge, "extra_charge_id"),
            )
            extra_c = create_new_camper_extra_charge(db, camper_schema)

    return extra_c
