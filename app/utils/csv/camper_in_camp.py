import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import csv

from model.camps import CamperInCamp, Camp
from model.campers import Camper, Parent
from model.user import User

CAMP_STATUS_ENROLLED_ID = int(os.getenv("CAMP_STATUS_ENROLLED_ID"))


def export_csv_camper_in_camp(db, camp_id:int):
    
    camper_in_camp = (db.query(Camper)
                      .join(Camper, Camper.id == CamperInCamp.camper_id)
                      .filter(and_(CamperInCamp.camp_id == camp_id, CamperInCamp.status == CAMP_STATUS_ENROLLED_ID))
                      .all()
                      )
    camp = db.query(Camp.name).filter(Camp.id==camp_id).first()

    filename = str(camp) + ".csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "description"])
        #for item in items:
        #    writer.writerow([item.id, item.name, item.description])

    return {"message": "CSV exported"}
