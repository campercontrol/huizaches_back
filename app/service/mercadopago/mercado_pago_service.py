from fastapi import APIRouter, Depends,Response, BackgroundTasks,UploadFile, Request
from sqlalchemy.orm import Session
from crud.mercadopago.mercadopago_crud import create_preference, get_merchant_order, get_payment
from utils.db import SessionLocal

mercadopago_routes = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@mercadopago_routes.get("/mercado_pago/create_payment_link/{camp_id}/{camper_id}/{customer_defined_amount}", tags=["mercadopago"])
def create_item(camp_id : int, camper_id: int, customer_defined_amount: int, db: Session = Depends(get_db)):
    response = create_preference(db, camp_id, camper_id, customer_defined_amount)
    return response
    

        
@mercadopago_routes.post("/mercado_pago/notify", tags=["mercadopago"])
async def mercado_pago_payment_notification(request: Request):
    try : 
        print(f'request json : {await request.json()}')
        # return request.body()
    except Exception as err:
        # could not parse json
        print(f'request body : {await request.body()}')
        # return request.body()
        


@mercadopago_routes.get("/mercadopago/merchant_order/{merchant_order_id}", tags=["mercadopago"])
def mercadopago_merchant_order(merchant_order_id: int, request: Request):
    response = get_merchant_order(merchant_order_id)
    return response



@mercadopago_routes.get("/mercadopago/payment/{payment_id}", tags=["mercadopago"])
def mercadopago_payment_id(payment_id: int, request: Request):
    response = get_payment(payment_id)
    return response
    
    
# @mercadopago_routes.post("/mercadopago/preference", tags=["mercadopago"])
# def mercadopago_preference(request: Request):
#     preference = sdk.preference().get()
#     print(preference)
#     return preference
    
    


# @mercadopago_routes.post("/something", tags=["mercadopago"])
# async def something(request: Request):
#     try : 
#         print(f'request json : {await request.json()}')
#     except Exception as err:
#         # could not parse json
#         print(f'request body : {await request.body()}')
#     return True
        

    