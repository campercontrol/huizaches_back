from sqlalchemy import case, and_
from sqlalchemy.orm import Session

from model.payments import Payment, PaymentTransactionType, PaymentMethod
from model.campers import Camper
from model.campers.parent import Parent
from model.camps import Camp, CamperInCamp

from utils.payments.payment_table import get_payment_table

from crud.payments.payment_method_crud import get_all_payment_method
from crud.payments.payment_transaction_type_crud import get_all_payment_transaction_type

from schema.payments.payment_schema import (
    PaymentCreate,
    PaymentModify,
)



def get_all_payment(db):
    rows = db.query(Payment).all()
    return rows


def get_payment_by_id(db, payment_id: int):
    return (
        db.query(Payment)
        .filter_by(
            id=payment_id,
        )
        .first()
    )

def create_payment_controller(db: Session, new_payment):
    try:
        create_new_payment_and_update_balance_transaction(db, new_payment.dict())
        db.commit()
        return 1
    except Exception as ex:
        db.rollback()
        print(ex)
        return 3
def create_new_payment(db, new_payment: PaymentCreate):
    db_payment = None
    try:
        if new_payment["payment_amount"] < 0:
            new_payment["payment_amount"] = new_payment["payment_amount"] * -1
        
        if new_payment["txn_type_id"] in (1,2,9):
            new_payment["payment_amount"] = new_payment["payment_amount"] * -1
        
        db_payment = Payment(**new_payment)
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
    except Exception as ex:
        db.rollback()
        print(f"An error ocurred while saving new payment {ex}")
    return db_payment    
    
def create_new_payment_and_update_balance(db, new_payment: PaymentCreate):
    camper_id = new_payment["camper_id"]
    camp_id = new_payment["camp_id"]
    camper_in_camp = db.query(CamperInCamp).filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.camper_id == camper_id)).first()
    try:
        
        if new_payment["payment_amount"] < 0:
            new_payment["payment_amount"] = new_payment["payment_amount"] * -1
        
        if new_payment["txn_type_id"] in (1,2,9):
            new_payment["payment_amount"] = new_payment["payment_amount"] * -1
        
        db_payment = Payment(**new_payment)
        db.add(db_payment)
        db.commit()
        if db_payment.txn_type_id in (1,2,9):
            total_balance = abs(camper_in_camp.payment_balance) - abs(float(db_payment.payment_amount))
            camper_in_camp.payment_balance = total_balance
            db.add(camper_in_camp) 
            db.commit()
        else:
            total_balance = abs(camper_in_camp.payment_balance) + abs(float(db_payment.payment_amount))
            camper_in_camp.payment_balance = total_balance
            db.add(camper_in_camp) 
            db.commit()            
        
        db.refresh(db_payment)
    except Exception as ex:
        db_payment = None
        db.rollback()
        print(f"An error ocurred while saving payment: {ex}")    
    return db_payment

def create_new_payment_and_update_balance_transaction(db, new_payment: PaymentCreate):
    camper_id = new_payment["camper_id"]
    camp_id = new_payment["camp_id"]
    camper_in_camp = db.query(CamperInCamp).filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.camper_id == camper_id)).first()
        
    if new_payment["payment_amount"] < 0:
        new_payment["payment_amount"] = new_payment["payment_amount"] * -1
    
    if new_payment["txn_type_id"] in (1,2,9):
        new_payment["payment_amount"] = new_payment["payment_amount"] * -1
    db_payment = Payment(**new_payment)
    print("new_payment_charged")
    db.add(db_payment)
    db.flush()
    if db_payment.txn_type_id in (1,2,9):
        total_balance = abs(camper_in_camp.payment_balance) - abs(float(db_payment.payment_amount))
        camper_in_camp.payment_balance = total_balance
        db.add(camper_in_camp) 
    else:
        total_balance = abs(camper_in_camp.payment_balance) + abs(float(db_payment.payment_amount))
        camper_in_camp.payment_balance = total_balance
        db.add(camper_in_camp) 
    db.flush()
    return db_payment
    

def delete_payment_and_update_balance_transaction(db: Session, payment_id: int, camper_id):
    payment = get_payment_by_id(db, payment_id)
    camper_in_camp = db.query(CamperInCamp).filter(and_(CamperInCamp.camp_id == payment.camp_id, CamperInCamp.camper_id == camper_id)).first()
    if payment.txn_type_id in (1,2,9):
        total_balance = abs(camper_in_camp.payment_balance) + abs(float(payment.payment_amount))
        camper_in_camp.payment_balance = total_balance
        db.add(camper_in_camp)
        db.delete(payment)
    else:
        total_balance = abs(camper_in_camp.payment_balance) - abs(float(payment.payment_amount))
        camper_in_camp.payment_balance = total_balance
        db.add(camper_in_camp) 
        db.delete(payment)        
        
def delete_payment_and_update_balance(db: Session, payment_id: int, camper_id):
    payment = get_payment_by_id(db, payment_id)
    camper_in_camp = db.query(CamperInCamp).filter(and_(CamperInCamp.camp_id == payment.camp_id, CamperInCamp.camper_id == camper_id)).first()
    try:
        if payment.txn_type_id in (1,2,9):
            total_balance = abs(camper_in_camp.payment_balance) + abs(float(payment.payment_amount))
            camper_in_camp.payment_balance = total_balance
            db.add(camper_in_camp)
            db.delete(payment)
            db.commit()
        else:
            total_balance = abs(camper_in_camp.payment_balance) - abs(float(payment.payment_amount))
            camper_in_camp.payment_balance = total_balance
            db.add(camper_in_camp) 
            db.delete(payment)
            db.commit()            
    except Exception as ex:     
        db.rollback()
        print(f"An error ocurred while saving payment: {ex}")
        return False
    return True            
        
def update_payment_by_id(db, payment_id: int, modify_payment: PaymentModify):
    rows_updated = (
        db.query(Payment)
        .filter_by(id=payment_id)
        .update(modify_payment, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated

        
def update_payment_controller(db, payment_id: int, modify_payment: PaymentModify):
    
    try:
        current_payment = db.query(Payment).filter(Payment.id == payment_id).first()
        camper_in_camp = db.query(CamperInCamp).filter(and_(CamperInCamp.camp_id == current_payment.camp_id, CamperInCamp.camper_id == current_payment.camper_id)).first()

        if current_payment.txn_type_id in (1,2,9,11):
            camper_in_camp.payment_balance += abs(current_payment.payment_amount)
        else:
            camper_in_camp.payment_balance -= abs(current_payment.payment_amount)
        
        if modify_payment.txn_type_id in (1,2,9):
            total_balance = abs(camper_in_camp.payment_balance) - abs(float(modify_payment.payment_amount))
            camper_in_camp.payment_balance = total_balance
            db.add(camper_in_camp) 
        else:
            total_balance = abs(camper_in_camp.payment_balance) + abs(float(modify_payment.payment_amount))
            camper_in_camp.payment_balance = total_balance
            db.add(camper_in_camp)
        
        db.query(Payment).filter_by(id=current_payment.id).update(modify_payment.dict(), synchronize_session="fetch")
        db.commit()
        return 1
    except Exception as ex:
        print(ex)
        db.rollback()
        return 3

def get_payment_by_camper_camp(db, camper_id: int, camp_id: int):
    rows = (
        db.query(
            Payment.id.label("id"),
            Payment.payment_amount.label("payment_amount"),
            Payment.payment_date.label("payment_date"),
            Payment.txn_number.label("txn_number"),
            PaymentMethod.name.label("payment_method"),
            PaymentTransactionType.name.label("txn_name"),
        )
        .select_from(Payment)
        .join(PaymentMethod, PaymentMethod.id == Payment.payment_method_id, isouter=True)
        .join(PaymentTransactionType, PaymentTransactionType.id == Payment.txn_type_id)
        .filter(and_(Payment.camper_id == camper_id, Payment.camp_id == camp_id))
        .order_by(Payment.payment_date.asc())
        .all()
    )
    payment_table = get_payment_table(db, rows)

    return payment_table

# imported here due to a circular import
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
    
def get_payment_page_camper_in_camp(
    db, camper_id: int, camp_id: int, camper_in_camp_id: int
):
    if (camper_id == 0 or camp_id == 0) and camper_in_camp_id != 0:
        camper_in_camp = (
            db.query(CamperInCamp).filter(CamperInCamp.id == camper_in_camp_id).first()
        )
        camper_id = getattr(camper_in_camp, "camper_id")
        camp_id = getattr(camper_in_camp, "camp_id")

    else:
        camper_in_camp = get_camper_in_camp_by_camper_camp(db, camper_id, camp_id)
        camper_in_camp_id = getattr(camper_in_camp, "id")

    payment_table = get_payment_by_camper_camp(db, camper_id, camp_id)

    camp_name = db.query(Camp.name).filter(Camp.id == camp_id).first()[0]
    camper = (
        db.query(
            (
                Camper.name
                + " "
                + Camper.lastname_father
                + " "
                + Camper.lastname_mother
            ).label("fullname"),
            Camper.parent_id.label("parent_id"),
        )
        .filter(Camper.id == camper_id)
        .first()
    )
    payment_methods = get_all_payment_method(db)
    transaction_type = get_all_payment_transaction_type(db)

    return {
        "payment_methods": payment_methods,
        "transaction_type": transaction_type,
        "camper_name": camper.fullname,
        "camp_name": camp_name,
        "camper_id": camper_id,
        "camp_id": camp_id,
        "camper_in_camp_id": camper_in_camp_id,
        "parent_id": camper.parent_id,
        "payment_balance": camper_in_camp.payment_balance,
        "payment_table": payment_table,
    }


def update_camper_balance_camper(db, camper_id: int, camp_id: int):
    camper_payments = db.query(Payment).filter(
        and_(Payment.camp_id == camp_id, Payment.camper_id == camper_id)).all()
    
    total_balance = 0
    if camper_payments:
        for payment in camper_payments:
            total_balance = total_balance + payment.payment_amount

    db.query(CamperInCamp).filter(
        and_(
            CamperInCamp.camp_id == camp_id, CamperInCamp.camper_id == camper_id
        )
    ).update({"payment_balance": total_balance})
    db.commit()
    
    return 1

def get_payment_transaction_type_by_movement(db: Session, movement_id):
    query = db.query(PaymentTransactionType.uid, 
                     PaymentTransactionType.id, 
                     PaymentTransactionType.name,
                     PaymentTransactionType.movement).filter(PaymentTransactionType.movement == movement_id)
    data = db.execute(query)
    return data.mappings().first()

def get_all_camper_payments(db: Session, camper_id):
    query = db.query(Payment.id,
                     Payment.payment_amount,
                     Payment.txn_number).filter(Payment.camper_id == camper_id)
    data = db.execute(query)
    data = data.mappings().all()
    return data

def apply_massive_payment(db: Session, camp_id: int, massivePayment):
    campers = massivePayment.campers
    new_payment = dict(massivePayment.payment)
    camp_data = db.query(Camp).filter(Camp.id == camp_id).first()
    new_payment["currency_id"] = camp_data.currency_id
    
    result = True
    for camper in campers:
        camper_in_camp = db.query(CamperInCamp).filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.camper_id == camper)).first()
        camper_data = db.query(Camper.id.label("camper_id"), Parent.id.label("parent_id")).select_from(Camper).join(Parent, Parent.id == Camper.parent_id).first()   
        new_payment["parent_id"] = camper_data.parent_id
        new_payment["camper_id"] = camper
        new_payment["camp_id"] = camp_id
        
        try:
            if new_payment["payment_amount"] < 0:
                new_payment["payment_amount"] = new_payment["payment_amount"] * -1
            
            if new_payment["txn_type_id"] in (1,2,9,11):
                new_payment["payment_amount"] = new_payment["payment_amount"] * -1
            
            db_payment = Payment(**new_payment)
            db.add(db_payment)
            db.commit()
            if db_payment.txn_type_id in (1,2,9):
                total_balance = abs(camper_in_camp.payment_balance) - abs(float(db_payment.payment_amount))
                camper_in_camp.payment_balance = total_balance
                db.add(camper_in_camp) 
                db.commit()
            else:
                total_balance = abs(camper_in_camp.payment_balance) + abs(float(db_payment.payment_amount))
                camper_in_camp.payment_balance = total_balance
                db.add(camper_in_camp) 
                db.commit()            
            
        except Exception as ex:
            db.rollback()
            result = False
            print(f"An error ocurred while saving payment: {ex}")    
        
    return result
    