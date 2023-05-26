from xmlrpc.client import boolean

from fastapi import APIRouter, Depends,Response, BackgroundTasks,UploadFile
from sqlalchemy.orm import Session
from utils.db import SessionLocal

from utils.pdf.camper_info import generar_pdf_info_camping, generar_pdf_info_camping_multiple, generar_pdf_info_camping_multiple_merge_files
from utils.pdf.baucher_pago import generar_pdf_baucher
from utils.pdf.bracelet import generar_pdf_bracelete,generar_pdf_bracelete_multiple

pdf_routes = APIRouter()

# Dependency


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@pdf_routes.get("/pdf/camper/info", tags=["pdf"])
def get_pdf_camper_info(
    db: Session = Depends(get_db)
):
    NAME = "get_pdf_camper_info"

    generar_pdf_info_camping()

    return {"data": "Ready"}


@pdf_routes.get("/pdf/camper/info/multiple", tags=["pdf"])
def get_pdf_camper_info_multiple(
    db: Session = Depends(get_db)
):
    NAME = "get_pdf_camper_info"

    generar_pdf_info_camping_multiple()

    return {"data": "Ready"}


@pdf_routes.get("/pdf/camper/info/multiple_merge", tags=["pdf"])
def get_pdf_camper_info_multiple_merge(
    db: Session = Depends(get_db)
):
    NAME = "get_pdf_camper_info"

    generar_pdf_info_camping_multiple_merge_files()

    return {"data": "Ready"}


@pdf_routes.get("/pdf/pagos/baucher", tags=["pdf"])
def get_pdf_baucher(
    db: Session = Depends(get_db)
):
    NAME = "get_pdf_baucher"

    generar_pdf_baucher()

    return {"data": "Ready"}


@pdf_routes.get("/pdf/pagos/bracelete", tags=["pdf"])
def get_pdf_bracelete(
    db: Session = Depends(get_db)
):
    NAME = "get_pdf_bracelete"

    generar_pdf_bracelete()

    return {"data": "Ready"}


@pdf_routes.get("/pdf/pagos/bracelete_multiple", tags=["pdf"])
def get_pdf_bracelete_multiple(
    db: Session = Depends(get_db)
):
    NAME = "get_pdf_bracelete"

    generar_pdf_bracelete_multiple()

    return {"data": "Ready"}