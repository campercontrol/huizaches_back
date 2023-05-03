from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.camps import Camp, Location
from model.campers import Camper
from schema.camps.camp_schema import CampCreate, CampModify
