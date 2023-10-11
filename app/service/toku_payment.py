
from fastapi import APIRouter, Depends,Response, BackgroundTasks,UploadFile, Request
from sqlalchemy.orm import Session

from utils.toku_payment_tools import *   
from schema.toku_payment import (
    CustomerTokuCreate, 
    InvoiceTokuCreate, 
    WebhookTokuCreate,
    PaymentsConsultTokuCreate
)

from datetime import datetime, timedelta
import json
import pytz

newMexZone = pytz.timezone("America/Mexico_City") 

toku_routes = APIRouter()


#Clientes --------------------------------->


@toku_routes.post("/toku/register_customer", tags=["Toku payment"])
def register_customer(customer:CustomerTokuCreate):
    NAME = "register_customer"
    response = create_customer("1","almazan@hotmail.com","Juan","+525580224021",False)
    # response = create_customer(
    #                   customer.external_id,
    #                   customer.email,
    #                   customer.name,
    #                   customer.phone,
    #                   customer.send_mail)
    print(response)
    response_json = json.loads(response.text)
    print(response_json)

    """
    Response [201]:
    {
        "external_id": "1",
        "government_id": null,
        "name": "Juan",
        "mail": "almazan@hotmail.com",
        "phone_number": "+525580224021",
        "silenced_until": null,
        "default_agent": null,
        "agent_phone_number": null,
        "pac_mandate_id": null,
        "send_mail": false,
        "default_receipt_type": "bill",
        "rfc": null,
        "tax_zip_code": null,
        "fiscal_regime": null,
        "secondary_emails": [],
        "metadata": {},
        "id": "cus_X361Zag0jybU4AG1qTv_XYSPYkXYa8IZ"
    }
    """

    return response_json


@toku_routes.get("/toku/get_customer/{customer_id}", tags=["Toku payment"])
def get_customer_by_id(customer_id:str):
    NAME = "get_customer_by_id"
    response = get_customer(customer_id)
    print(response)
    response_json = json.loads(response.text)
    print(response_json)

    """
    Response [200]
    {
        "external_id": "1",
        "government_id": null,
        "name": "Juan",
        "mail": "almazan@hotmail.com",
        "phone_number": "+525580224021",
        "silenced_until": null,
        "default_agent": null,
        "agent_phone_number": null,
        "pac_mandate_id": null,
        "send_mail": false,
        "default_receipt_type": "bill",
        "rfc": null,
        "tax_zip_code": null,
        "fiscal_regime": null,
        "secondary_emails": [],
        "metadata": {},
        "id": "cus_X361Zag0jybU4AG1qTv_XYSPYkXYa8IZ"
    }
    """

    return response_json


@toku_routes.post("/toku/create_invoice", tags=["Toku payment"])
def create_invoice_producto(invoice:InvoiceTokuCreate):
    NAME = "create_producto"
    response = create_invoice(
                customer_id = "cus_X361Zag0jybU4AG1qTv_XYSPYkXYa8IZ",
                product_id = "1",
                due_date = "2023-10-30",#YYYY-MM-DD #fecha de vencimiento
                amount= "100"
    )
    # response = create_invoice(
    #             customer_id = invoice.customer_id,
    #             product_id = invoice.product_id,
    #             due_date = invoice.due_date,#YYYY-MM-DD #fecha de vencimiento
    #             amount = invoice.amount
    # )
    print(response)
    response_json = json.loads(response.text)
    print(response_json)

    """
    {
        "customer": "cus_X361Zag0jybU4AG1qTv_XYSPYkXYa8IZ",
        "product_id": "1",
        "subscription": "sub_zTo9oCMo-f0_KIs-CcDwM1_FUdVji8r1",
        "is_paid": false,
        "due_date": "2023-10-30",
        "is_void": false,
        "amount": 100.0,
        "link_payment": "https://kincampsandbox.trytoku.com/dashboard?user=cus_X361Zag0jybU4AG1qTv_XYSPYkXYa8IZ",
        "metadata": {
            
        },
        "receipt_type": null,
        "id_receipt": null,
        "source": null,
        "disable_automatic_payment": false,
        "currency_code": "MXN",
        "invoice_external_id": "1-2023-10-30",
        "id": "in_gcmcVYdWdGAKIVF3IN-zDgz2ILA01F2H"
    }
    """

    return response_json


@toku_routes.post("/toku/create_webhook", tags=["Toku payment"])
def create_webhook(webhook:WebhookTokuCreate):
    NAME = "create_producto"
    response = create_webhook_toku(
        webhook.enabled_events,
        webhook.status,
        webhook.url
        )
    print(response)
    response_json = json.loads(response.text)
    print(response_json)

    """
    {
    "enabled_events": [
        "interaction.incoming",
        "interaction.outgoing",
        "payment_method.attached",
        "payment_method.attached_products",
        "payment_method_inscription_intent.failed",
        "payment_intent.succeeded",
        "payment_intent.payment_failed",
        "payment_intent.succeeded_batch",
        "payment_intent.payment_failed_batch",
        "payment_intent.payment_pending_batch",
        "payment.succeeded",
        "activation.created",
        "bank_account_verification.result",
        "payout.done"
    ],
    "url": "https://9366-189-217-208-160.ngrok-free.app/toku/webhook_listener",
    "status": "enabled",
    "id": "whe_4zYGCpAdfjJivnZbq9UHgYtIYVRsTnNh",
    "secret": "whesec_LD7BeNFGQRZ0FvjkVt5WL3RiNFv4c0Cd"
    }
    """

    return response_json


@toku_routes.post("/toku/webhook_listener", tags=["Toku payment"])
async def listen_webhook(request: Request):
    NAME = "listen_clicks_webhook"
    datos = await request.body()
    print(datos)
    return []


    #     {
    #   'enabled_events': [
    #     'interaction.incoming',
    #     'interaction.outgoing',
    #     'payment_method.attached',
    #     'payment_method.attached_products',
    #     'payment_method_inscription_intent.failed',
    #     'payment_intent.succeeded',
    #     'payment_intent.payment_failed',
    #     'payment_intent.succeeded_batch',
    #     'payment_intent.payment_failed_batch',
    #     'payment_intent.payment_pending_batch',
    #     'payment.succeeded',
    #     'activation.created',
    #     'bank_account_verification.result',
    #     'payout.done'
    #   ],
    #   'url': 'https://9366-189-217-208-160.ngrok-free.app/toku/webhook_listener',
    #   'status': 'enabled',
    #   'id': 'whe_4zYGCpAdfjJivnZbq9UHgYtIYVRsTnNh',
    #   'secret': 'whesec_LD7BeNFGQRZ0FvjkVt5WL3RiNFv4c0Cd'
    # }


@toku_routes.post("/toku/check_payments", tags=["Toku payment"])
def get_payments_by_page(payment:PaymentsConsultTokuCreate):

    NAME = "get_payments_by_page"
    response = get_payments(payment.page,payment.page_size,payment.start_date,payment.end_date)
    print(response)
    response_json = json.loads(response.text)
    print(response_json)

    return response_json

    



