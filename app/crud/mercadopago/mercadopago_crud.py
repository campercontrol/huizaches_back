import uuid
import os
from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import date, datetime
from fastapi import Request
from crud.camps.camp_crud import get_camp_by_id
from model.campers import Camper, Parent
from model.camps.camp import Camp
from model.catalogs.currency import Currency
from model.mercadopago import MercadopagoMerchantOrder, MercadopagoPayment, MercadopagoPreference
from utils.db import db_mapping_rows_to_dict
from model.user import User
from crud.payments.payment_crud import create_new_payment_and_update_balance_transaction
from schema.mercadopago.mercadopago_payment_schema import MercadopagoPaymentCreate, MercadopagoPaymentUpdate
from schema.mercadopago.mercadopago_merchant_order_schema import MercadopagoMerchantOrderCreate
from schema.payments.payment_schema import PaymentCreate
# SDK de Mercado Pago
import mercadopago
# Agrega credenciales
mp_token = os.getenv("MP_TOKEN")
sdk = mercadopago.SDK(mp_token)


def get_customer_info(db: Session, camper_id: int):
    query = db.query(Camper.id.label("camper_id"),
                     Camper.name,
                     Camper.lastname_father,
                     Camper.lastname_mother,
                     Parent.id.label("parent_id"),
                     Parent.tutor_name,
                     Parent.tutor_lastname_father,
                     Parent.tutor_lastname_mother,
                     Parent.contact_cellphone,
                     User.email
                     ).select_from(Camper).join(Parent, Parent.id == Camper.parent_id).join(User, User.id == Parent.user_id).where(Camper.id == camper_id)
    data = db.execute(query)
    data = data.mappings().first()
    return data


def get_camp_info(db: Session, camp_id: int):
    query = db.query(Camp.id,
                     Camp.name,
                     Camp.currency_id,
                     Currency.name.label("currency_name")
                     ).select_from(Camp).join(Currency, Currency.id == Camp.currency_id).where(Camp.id == camp_id)
    data = db.execute(query)
    data = data.mappings().first()
    return data

def get_preference(preference_id : int):
    preference_response = sdk.preference().get(preference_id)
    print(preference_response)
    if preference_response["status"] == 404:
        return None
    if preference_response["status"] == 200:
        preference = preference_response["response"]
        return preference
    return None

def get_internal_preference_by_preference_id(db: Session, preference_id: int):
    preference = db.query(MercadopagoPreference).filter(MercadopagoPreference.preference_id == preference_id).first()
    return preference


def get_mercadopago_merchant_order(merchant_order_id : int):
    merchant_order_response = sdk.merchant_order().get(merchant_order_id)
    if merchant_order_response["status"] == 404:
        return None
    if merchant_order_response["status"] == 200:
        merchant_order = merchant_order_response["response"]
        return merchant_order
    return None

def get_internal_merchant_order_by_id(db: Session, merchant_order_id: int):
    merchant_order = db.query(MercadopagoMerchantOrder).filter(MercadopagoMerchantOrder.merchant_order_id == merchant_order_id).first()
    return merchant_order

def get_internal_mercadopago_payment_by_id(db: Session, payment_id: int):
    payment = db.query(MercadopagoPayment).filter(MercadopagoPayment.payment_id == payment_id).first()
    return payment

def get_internal_mercadopago_merchant_order_by_merchant_order_id(db: Session, merchant_order_id: int):
    merchant_order = db.query(MercadopagoMerchantOrder).filter(MercadopagoMerchantOrder.merchant_order_id == merchant_order_id).first()
    return merchant_order

def create_internal_mercadopago_payment(db: Session, new_internal_mercadopago_payment: MercadopagoPaymentCreate): 
    db_internal_mercadopago_payment = MercadopagoPayment(
        **new_internal_mercadopago_payment
        )
    db.add(db_internal_mercadopago_payment)
    db.flush()
    return db_internal_mercadopago_payment

def create_internal_mercadopago_merchant_order(db: Session, new_internal_mercadopago_merchant_order: MercadopagoMerchantOrderCreate): 
    db_internal_mercadopago_merchant_order = MercadopagoMerchantOrder(
        **new_internal_mercadopago_merchant_order
    )
    db.add(db_internal_mercadopago_merchant_order)
    db.flush()
    return db_internal_mercadopago_merchant_order

def update_internal_mercadopago_payment(db, mercadopago_internal_payment_id: int, modify_mercadopago_internal_payment: MercadopagoPaymentUpdate):
    record_updated = (
        db.query(MercadopagoPayment)
        .filter(MercadopagoPayment.id == mercadopago_internal_payment_id)
        .update(modify_mercadopago_internal_payment, synchronize_session="fetch")
    )
    db.commit()
    return record_updated

def get_payment(payment_id : int):
    payment_response = sdk.payment().get(payment_id)
    if payment_response["status"] == 404:
        return None
    if payment_response["status"] == 200:    
        payment = payment_response["response"]
        return payment
    return None

def get_mercado_pago_payments_by_camp_id_and_camper_id(db: Session, camp_id: int, camper_id: int):
    
    camp_camper_mercadopago_payments_query = db.query(MercadopagoPayment.payment_id).filter(and_(MercadopagoPayment.camp_id == camp_id, MercadopagoPayment.camper_id == camper_id))
    camp_camper_mercadopago_payments = db.execute(camp_camper_mercadopago_payments_query)
    camp_camper_mercadopago_payments = camp_camper_mercadopago_payments.mappings().all()
    
    payments = []
    for camp_camper_mercadopago_payment in camp_camper_mercadopago_payments:
        payment = get_payment(camp_camper_mercadopago_payment["payment_id"])
        payments.append(payment)
    return payments     

async def process_notification(db: Session, request: Request):
    try: 
        request = await request.json()
        print(request)
        if request["type"] == "payment":
            payment_id = request["data"]["id"]
            mercadopago_payment = get_payment(payment_id)
            internal_mercadopago_payment = get_internal_mercadopago_payment_by_id(db, payment_id)
                
            mercadopago_merchant_order = get_mercadopago_merchant_order(mercadopago_payment["order"]["id"])
            internal_mercadopago_merchant_order = get_internal_mercadopago_merchant_order_by_merchant_order_id(db, mercadopago_merchant_order["id"])

            new_internal_mercadopago_merchant_order = {
                "merchant_order_id": mercadopago_merchant_order["id"],
                "external_id": mercadopago_merchant_order["external_reference"],
                "status": mercadopago_merchant_order["status"],
                "camper_id": mercadopago_payment["metadata"]["customer"]["camper_id"],
                "camp_id": mercadopago_payment["metadata"]["camp"]["id"]
            }
            if not internal_mercadopago_merchant_order:
                create_internal_mercadopago_merchant_order(db, new_internal_mercadopago_merchant_order)
            else:
                internal_mercadopago_merchant_order.status = mercadopago_merchant_order["status"]
                
            internal_payment = {
                
                "paid": True,
                "payment_amount": int(mercadopago_payment["transaction_details"]["total_paid_amount"]),
                "txn_number": "Pago de campamento (Mercadopago)"  + " " + mercadopago_payment["metadata"]["customer"]["name"] + " " +
                mercadopago_payment["metadata"]["customer"]["lastname_father"] + " " + mercadopago_payment["metadata"]["customer"]["lastname_mother"],
                "camp_id": mercadopago_payment["metadata"]["camp"]["id"],
                "payment_date": datetime.now(),
                "payment_method_id": 10,
                "camper_id": mercadopago_payment["metadata"]["customer"]["camper_id"],
                "currency_id": mercadopago_payment["metadata"]["camp"]["currency_id"],
                "parent_id": mercadopago_payment["metadata"]["customer"]["parent_id"],
                "txn_type_id": 3                     
            }
                
            if not internal_mercadopago_payment:
                new_internal_mercadopago_payment = {    
                    "status" : mercadopago_payment["status"],
                    "payment_id" : mercadopago_payment["id"],
                    "external_id" : mercadopago_payment["external_reference"],
                    "camper_id" : mercadopago_payment["metadata"]["customer"]["camper_id"],
                    "camp_id" : mercadopago_payment["metadata"]["camp"]["id"]
                
                }
                    
                if mercadopago_payment["status"] == "approved":                    
                    internal_payment_created = create_new_payment_and_update_balance_transaction(db, internal_payment)
                    new_internal_mercadopago_payment["internal_payment_id"] = internal_payment_created.id
                    create_internal_mercadopago_payment(db, new_internal_mercadopago_payment)
                else:
                    create_internal_mercadopago_payment(db, new_internal_mercadopago_payment)
                    
            else:
                if mercadopago_payment["status"] == "approved":
                    if internal_mercadopago_payment.internal_payment_id is None:
                        internal_payment_created = create_new_payment_and_update_balance_transaction(db, internal_payment)
                        internal_mercadopago_payment.status = mercadopago_payment["status"]
                        internal_mercadopago_payment.internal_payment_id = internal_payment_created.id
                    else:
                        internal_mercadopago_payment.status = mercadopago_payment["status"]
        db.commit()    
        return 1
    except Exception as ex:
        db.rollback()
        print(ex)
        return 3
              


def create_preference(db: Session, camp_id: int, camper_id: int, customer_defined_amount: int):
    try:
        camp_info = get_camp_info(db, camp_id) 
        customer_info = get_customer_info(db, camper_id)    
        id = uuid.uuid4()
        id = str(id)
        metadata = {
            "customer": dict(customer_info),
            "camp": dict(camp_info)
        }  

        request = {
            "items": [
                {
                    "id": id,
                    "title": camp_info['name'],
                    "description": camp_info['name'] + " - " + customer_info['name'] + " " + customer_info['lastname_father'] + " " + customer_info['lastname_mother'],
                    "currency_id": camp_info['currency_name'],
                    "unit_price": customer_defined_amount,
                    "quantity": 1
                }
            ],
            # "marketplace_fee": 0,
            "payer": {
                "name": customer_info['tutor_name'],
                "surname": customer_info['tutor_lastname_father'] + customer_info['tutor_lastname_mother'],
                "email": customer_info['email'],
                "phone": {
                    "number": customer_info['contact_cellphone'],
                },
                # "identification": {
                #     "type": "CPF",s
                #     "number": "19119119100",
                # },
                # "address": {
                #     "zip_code": "",
                #     "street_name": "Street",
                #     "street_number": 123,
                # },
            },
            "back_urls": {
                "success": "https://app.campercontrol.com/mercado_pago_success",
                "failure": "https://app.campercontrol.com/mercado_pago_failure",
                "pending": "https://app.campercontrol.com/mercado_pago_pending",
            },
            # "differential_pricing": {
            #     "id": 1,
            # },
            "expires": False,
            # "additional_info": "Discount: 12.00",
            "auto_return": "all",
            "binary_mode": True,
            "external_reference": id,
            # "marketplace": "marketplace",
            "notification_url": "https://app.campercontrol.com:5050/mercado_pago/notify?source_news=webhooks",
            # "operation_type": "regular_payment",
            "payment_methods": {
                # "default_payment_method_id": "master",
                # "excluded_payment_types": [
                #     {
                #         "id": "ticket",
                #     },
                # ],
                # "excluded_payment_methods": [
                #     {
                #         "id": "",
                #     },
                # ],
                "installments": 3,
                "default_installments": 1,
            },
            "metadata": metadata
            # "statement_descriptor": "Test Store",
        }
        preference_response = sdk.preference().create(request)
        preference = preference_response["response"]
        mercadopago_internal_preference = MercadopagoPreference(
            preference_id= preference["id"],
            external_id = preference["external_reference"],
            camper_id = camper_id,
            camp_id = camp_id
        )
        db.add(mercadopago_internal_preference)
        db.commit()
    except Exception as ex:
        db.rollback()
        print(ex)
        return None
    return preference