from sqlalchemy import case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict
from datetime import date

from model.catalogs import (
    Vaccine,
    LicensedMedicine,
    FoodRestriction,
    PathologicalBackground,
    PathologicalBackgroundFamily,
)

def update_order_catalogs(db, list, catalog_type:int):
    if catalog_type ==  1:
        for l in list:
            food_res = db.query(FoodRestriction).filter(FoodRestriction.id == l['id']).first()
            food_res.order = l['order']
            db.commit()
    elif catalog_type == 2:
	    for l in list:
                food_res = db.query(Vaccine).filter(Vaccine.id == l['id']).first()
                food_res.order = l['order']
                db.commit()
    elif catalog_type ==  3:   
	    for l in list:
                food_res = db.query(LicensedMedicine).filter(LicensedMedicine.id == l['id']).first()
                food_res.order = l['order']
                db.commit()
    elif catalog_type ==  4:
	    for l in list:
                food_res = db.query(PathologicalBackground).filter(PathologicalBackground.id == l['id']).first()
                food_res.order = l['order']
                db.commit()
    elif catalog_type ==  5:
	    for l in list:
                food_res = db.query(PathologicalBackgroundFamily).filter(PathologicalBackgroundFamily.id == l['id']).first()
                food_res.order = l['order']
                db.commit()

    return "Update correctly"
