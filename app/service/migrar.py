
from fastapi import APIRouter, Depends,Response, BackgroundTasks,UploadFile, Request
from sqlalchemy.orm import Session

from utils.migrar_base import migrar_base_v2_to_v3
from utils.db import SessionLocal

from datetime import datetime, timedelta
import json
import pytz

newMexZone = pytz.timezone("America/Mexico_City") 

migrar_routes = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@migrar_routes.get("/migrar", tags=["Migracion"])
def migrar_base_v2(db: Session = Depends(get_db)):
    NAME = "migrar_base_v2"
    response = migrar_base_v2_to_v3(db)
    return response


   