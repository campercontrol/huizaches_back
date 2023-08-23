from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse


from crud.campers.parent_crud import (
    get_all_parent,
    get_parent_by_uuid,
    create_new_parent,
    create_new_parent_user_id,
    update_parent_by_id,
    delete_parent, 
    search_parent_by_name_user
)    
from crud.camps.camp_crud import (
    get_camp_by_id
)
from crud.camps.location_crud import (
    get_location_by_uuid
)
from crud.camps.camper_in_camp_crud import (
    get_camper_in_camp_by_camper_camp,
    get_camps_name_amount_camper
)
from crud.payments.payment_crud import (
    get_payment_by_camper_camp
)
from crud.campers.camper_crud import (
    get_campers_from_parent,
    get_camper_by_uuid
)
from schema.campers.parent_schema import(
    ParentCreate,
    ParentModify,
    ParentCompleteCreate

)

from crud.crud_user import create_new_user
from utils.db import SessionLocal
from utils.image_tools import img_to_base_64
from utils.pdf.baucher_pago import generar_pdf_baucher

parent_routes = APIRouter()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@parent_routes.get("/parent/", tags=["Campers"])
def get_parent(db: Session = Depends(get_db)):
    list_parent = get_all_parent(db)
    return {"data": list_parent}

@parent_routes.get("/parent/{parent_id}", tags=["Campers"])
def get_parent_by_id(parent_id:str, db: Session = Depends(get_db)):
    list_parent = get_parent_by_uuid(db, parent_id)
    return {"data": list_parent}

@parent_routes.post("/parent/", tags=["Campers"])
def create_parent(new_parent:ParentCreate, db: Session =Depends(get_db)):
    list_parent = create_new_parent(db, new_parent)
    return {"data": list_parent}

@parent_routes.post("/parent_create/", tags=["Campers"])
def create_parent_complete(new_parent_complete:ParentCompleteCreate, db: Session =Depends(get_db)):
    user = create_new_user(db, new_parent_complete.user)
    parent = create_new_parent_user_id(db, new_parent_complete.parent, user.id)
    return {"data": parent}

@parent_routes.patch("/parent/{parent_id}", tags=["Campers"])
def update_parent(parent_id:str,modify_parent:ParentModify,db: Session = Depends(get_db)):

    update_data = modify_parent.dict(exclude_unset=True)
    print(update_data)
    parent_upcdate_result = update_parent_by_id(db,parent_id,update_data)

    if parent_upcdate_result != 0:
        exist_parent = get_parent_by_uuid(db, parent_id)
        return {"mensaje": "Actualizado Correctamente", "data": exist_parent}
    else:
        return {"mensaje": "Ningun registro fue afectado", "data": ""}
        
@parent_routes.get("/parent_dashboard/{parent_id}", tags=["Campers"])
def parent_dashboard(parent_id:int, db: Session = Depends(get_db)):
    info = []
    parent_total_amount = 0
    list_campers= get_campers_from_parent(db, parent_id)
    for camper in list_campers:
        total_amount = 0
        camps_info = get_camps_name_amount_camper(db, camper.get('id'))
        for camp in camps_info:
            total_amount = total_amount + camp.get('camper_payment_balance')
        info.append(
            {
                "camper": camper,
                "camper_balance": total_amount,
                "camps": camps_info
            }
        )
        parent_total_amount = parent_total_amount + total_amount
    return{
            "parent_total_amount": parent_total_amount,
            "campers": info            
        }

@parent_routes.get("/parent_camper_in_camp/{camper_id}/{camp_id}", tags=["Campers"])
def parent_camper_in_camp(camper_id:int, camp_id:int,  db: Session = Depends(get_db)):
    camp= get_camp_by_id(db, camp_id)
    location = get_location_by_uuid(db, camp.location_id)
    payments= get_payment_by_camper_camp(db, camper_id, camp_id)
    camper_in_camp = get_camper_in_camp_by_camper_camp(db, camper_id, camp_id)

    if camper_in_camp:
        camper_subscribe = True
    else:
        camper_subscribe = False

    if camp.show_payment_parent and camper_subscribe:
        return{"camper_subscribe": camper_subscribe, "camp": camp, "location": location.name,  "payments":payments, "payment_balance": camper_in_camp.payment_balance}
    else:
        return{"camper_subscribe": camper_subscribe, "camp": camp, "location": location.name}

@parent_routes.delete("/delete_parent/{parent_id}", tags=["Campers"])
def delete_parent_by_id(parent_id:int, db: Session = Depends(get_db)):
    status = delete_parent(db, parent_id)
    return{"status": status}

@parent_routes.get("/search/parent/{search}", tags=["Campers"])
def get_search_parent(search:str, db: Session = Depends(get_db)):
    possible_parents  = search_parent_by_name_user(db, search)
    return { "data": possible_parents }

@parent_routes.get("/payment_boucher/{camper_id}/{camp_id}", response_class=FileResponse, tags=["Campers"])
def get_payment_boucher(camper_id:int, camp_id:int, db:Session= Depends(get_db)):
    camp = get_camp_by_id(db, camp_id)
    camper = get_camper_by_uuid(db, camper_id)
    camper_in_camp = get_camper_in_camp_by_camper_camp(db, camper_id, camp_id)
    logo_64 = "data:image/png;base64," + img_to_base_64("media/templates_pdf/logo/kincamp_logo_color.png").decode("utf-8")
    context = {
    "name_camping": getattr(camper, "name") + " " + getattr(camper, "lastname_father"),
    "camping_name":  getattr(camp, "name"),
    "amount_total": "$" + str(getattr(camp, "public_price")),
    "logo":logo_64,
    "information_accounts":[
        {
        "bank":"BBVA",
        "name_reference":"Angela Patricia Avila Rojas",
        "account_number":"0199909435",
        "clabe":"012180001999094351",
        },
         {
        "bank":"BBVA",
        "name_reference":"Angela Patricia Avila Rojas",
        "account_number":"0199909435",
        "clabe":"012180001999094351",
        }
    ],
    "pay_reference": str(getattr(camper_in_camp, "id")).zfill(6),
    "more_info": getattr(camp,"url"),
    "email":"pagos@kincamp.com"
    }   
    
    path = generar_pdf_baucher(context)
    return FileResponse(path)
