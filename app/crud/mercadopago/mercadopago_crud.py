import uuid
import os
from sqlalchemy.orm import Session

from crud.camps.camp_crud import get_camp_by_id
from model.campers import Camper, Parent
from model.camps.camp import Camp
from model.mercadopago import MercadopagoMerchantOrder, MercadopagoPayment
from utils.db import db_mapping_rows_to_dict
from model.user import User

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
                     Camp.name
                     ).where(Camp.id == camp_id)
    data = db.execute(query)
    data = data.mappings().first()
    return data
    

def get_merchant_order(merchant_order_id : int):
    merchant_order_response = sdk.merchant_order().get(merchant_order_id)
    merchant_order = merchant_order_response["response"]
    print(merchant_order)
    return merchant_order

def get_internal_merchant_order_by_id(db: Session, merchant_order_id: int):
    merchant_order = db.query(MercadopagoMerchantOrder).filter(MercadopagoMerchantOrder.merchant_order_id == merchant_order_id).first()
    return merchant_order

def get_internal_payment_by_id(db: Session, payment_id: int):
    payment = db.query(MercadopagoPayment).filter(MercadopagoPayment.payment_id == payment_id).first()
    return payment

def get_payment(payment_id : int):
    merchant_order_response = sdk.payment().get(payment_id)
    merchant_order = merchant_order_response["response"]
    print(merchant_order)
    return merchant_order
    

def create_preference(db: Session, camp_id: int, camper_id: int, customer_defined_amount: int):
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
			    "currency_id": "MXN",
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
                "area_code": 52,
                "number": customer_info['contact_cellphone'],
            },
            # "identification": {
            #     "type": "CPF",
            #     "number": "19119119100",
            # },
            # "address": {
            #     "zip_code": "",
            #     "street_name": "Street",
            #     "street_number": 123,
            # },
        },
        "back_urls": {
            "success": "http://migracion.campercontrol.com/mercado_pago_success",
            "failure": "http://migracion.campercontrol.com/mercado_pago_failure",
            "pending": "http://migracion.campercontrol.com/mercado_pago_pending",
        },
        # "differential_pricing": {
        #     "id": 1,
        # },
        "expires": False,
        # "additional_info": "Discount: 12.00",
        "auto_return": "all",
        "binary_mode": True,
        # "external_reference": "2",
        # "marketplace": "marketplace",
        "notification_url": "https://822f-201-141-109-215.ngrok-free.app/mercado_pago/notify",
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
    print(preference)
    return preference