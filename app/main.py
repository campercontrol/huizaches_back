from fastapi import FastAPI
from service.prueba_service import prueba_routes
from service.catalogs.currency_service import currency_routes
from service.catalogs.vaccine_service import vaccine_routes
from service.catalogs.food_restriction_service import food_restriction_routes
from service.catalogs.licensed_medicine_service import licensed_medicine_routes
from service.catalogs.pathological_back_fm_service import pathological_background_family_routes
from service.catalogs.pathological_back_service import pathological_background_routes
from service.catalogs.constant_service import constant_routes
from service.catalogs.payment_account_service  import payment_account_routes
from service.catalogs.staff_role_service import staff_role_routes
from service.campers.school_service import school_routes
from service.campers.parent_service import parent_routes
from service.campers.camper_service import camper_routes
from service.camps.location_service import location_routes
from service.camps.season_service import season_routes
from service.camps.camp_service import camp_router
from service.camps.camp_extra_charge_service import extra_charge_routes
from service.campers.camper_extra_question_service import extra_answer_routes

app = FastAPI()

app.include_router(prueba_routes)  # Login
app.include_router(currency_routes)
app.include_router(vaccine_routes)
app.include_router(food_restriction_routes)
app.include_router(licensed_medicine_routes)
app.include_router(pathological_background_routes)
app.include_router(pathological_background_family_routes)
app.include_router(constant_routes)
app.include_router(payment_account_routes)
app.include_router(staff_role_routes)
app.include_router(school_routes)
app.include_router(parent_routes)
app.include_router(camper_routes)
app.include_router(location_routes)
app.include_router(season_routes)
app.include_router(camp_router)
app.include_router(extra_charge_routes)
app.include_router(extra_answer_routes)

from service.role import role_routes
from service.user import user_routes
from service.token import token_routes
from service.image import image_routes

app.include_router(role_routes) # Role
app.include_router(user_routes) # User
app.include_router(token_routes) # token
app.include_router(image_routes) # Image


@app.post("/", )
def root_test():
    return "Cadena de prueba"