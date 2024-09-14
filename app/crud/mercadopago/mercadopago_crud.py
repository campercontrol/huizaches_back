import uuid
import os
from sqlalchemy import case
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict

from crud.camps.camp_crud import get_camp_by_id
from model.campers import Camper, School, CamperRecord, Parent
from model.user import User

# SDK de Mercado Pago
import mercadopago
# Agrega credenciales
mp_token = os.getenv("MP_TOKEN")
sdk = mercadopago.SDK(mp_token)


def get_customer_info(db: Session, camper_id: int):
    query = db.query(Camper, Parent, User).select_from(Camper).join(Parent, Parent.id == Camper.parent_id).join(User, User.id == Parent.user_id).where(Camper.id == camper_id)
    data = db.execute(query)
    data = data.mappings().first()
    return data


def get_merchant_order(merchant_order_id : int):
    merchant_order_response = sdk.merchant_order().get(merchant_order_id)
    merchant_order = merchant_order_response["response"]
    print(merchant_order)
    return merchant_order


def get_payment(payment_id : int):
    merchant_order_response = sdk.payment().get(payment_id)
    merchant_order = merchant_order_response["response"]
    print(merchant_order)
    return merchant_order
    

def create_preference(db: Session, camp_id: int, camper_id: int, customer_defined_amount: int):
    camp_info = get_camp_by_id(db, camp_id) 
    customer_info = get_customer_info(db, camper_id)    
    id = uuid.uuid4()
    id = str(id)
    
    request = {
        "items": [
            {
			    "id": id,
			    "title": camp_info.name,
			    "description": f'{camp_info.name} - {customer_info.Camper.name} {customer_info.Camper.lastname_father} {customer_info.Camper.lastname_mother}',
			    "currency_id": "MXN",
			    "unit_price": customer_defined_amount,
       			"quantity": 1
		    }
        ],
        # "marketplace_fee": 0,
        "payer": {
            "name": f'{customer_info.Parent.tutor_name}',
            "surname": f'{customer_info.Parent.tutor_lastname_father} {customer_info.Parent.tutor_lastname_mother}',
            "email": customer_info.User.email,
            "phone": {
                "area_code": 52,
                "number": customer_info.Parent.contact_cellphone,
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
        "notification_url": "https://4dea-201-141-18-223.ngrok-free.app/mercado_pago/notify",
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
        }
        # "statement_descriptor": "Test Store",
    }

    preference_response = sdk.preference().create(request)
    preference = preference_response["response"]
    print(preference)
    return preference