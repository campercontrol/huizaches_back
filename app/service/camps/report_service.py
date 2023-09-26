from xmlrpc.client import boolean

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from crud.camps.camper_in_camp_crud import get_campers_for_bracelets
from crud.camps.camp_crud import get_camp_by_id

from utils.pdf.bracelet import generar_pdf_bracelete_multiple, generar_pdf_bracelete
from utils.pdf.camper_info import generar_pdf_info_camping

from utils.db import SessionLocal

report_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@report_routes.get("/camp/bracelets/{camp_id}", tags=["Reports"])
def get_bracelets_camp(camp_id: int, db: Session = Depends(get_db)):
    campers = get_campers_for_bracelets(db, camp_id)
    camp = get_camp_by_id(db, camp_id)
    path = generar_pdf_bracelete_multiple(campers, getattr(camp, "name"))
    return FileResponse(path)


@report_routes.get("/camp/bracelets/zt230/{camp_id}", tags=["Reports"])
def get_bracelets_camp_zt230(camp_id: int, db: Session = Depends(get_db)):
    campers = get_campers_for_bracelets(db, camp_id)
    camp = get_camp_by_id(db, camp_id)
    path = generar_pdf_bracelete(campers, getattr(camp, "name"))
    return FileResponse(path)


@report_routes.get("/report/camperincamp/pdf/{camp_id}", tags=["Reports"])
def get_report_pdf_camp(camp_id: int, db: Session = Depends(get_db)):
    path = generar_pdf_info_camping()

    return FileResponse(path)
