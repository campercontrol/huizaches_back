from sqlalchemy.orm import Session
from model.groupings.grouping_camper import GroupingCamper
from model.groupings.grouping_camp import GroupingCamp
from model.campers.camper import Camper
from model.catalogs.constant import Constant
from model.camps import CamperInCamp
from fastapi import HTTPException
from schema.groupings.grouping_camper_schema import (
    GroupingCamperCreate,
    GroupingCamperUpdate,
)


def get_all_grouping_campers(db: Session):
    return db.query(GroupingCamper).all()


def get_grouping_camper_by_id(db: Session, grouping_camper_id: int):
    return (
        db.query(GroupingCamper).filter(GroupingCamper.id == grouping_camper_id).first()
    )


def create_new_grouping_camper(db: Session, grouping_camper: GroupingCamperCreate):
    db.begin()
    try:
        grouping_camp_row = db.query(GroupingCamp).filter(GroupingCamp.id == grouping_camper.grouping_camp_id).first()
        grouping_current_capacity = db.query(GroupingCamper).filter(GroupingCamper.grouping_camp_id == grouping_camper.grouping_camp_id).count()

        if grouping_camp_row == None:
            return {"detail": "No se econtró el grouping_camp_id"}        

        if grouping_current_capacity >= grouping_camp_row.maximum_capacity:
            return {"detail": "La agrupación ya se encuentra a su máxima capacidad"}

        search_grouping_camper = db.query(GroupingCamper).filter(GroupingCamper.camper_id == grouping_camper.camper_id, GroupingCamper.grouping_camp_id == grouping_camper.grouping_camp_id).first()
        
        if  not search_grouping_camper == None:
            return {"detail": "El camper ya se encuentra en la agrupación"}
        
        db_grouping_camper = GroupingCamper(**grouping_camper.dict())
        db.add(db_grouping_camper)
        
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    else:
        db.commit()
        db.refresh(db_grouping_camper)
    db.close()
    return db_grouping_camper
    

def assign_grouping_camp_to_campers(db: Session, campers_id, grouping_camp_id):
    for camper in campers_id:
        actual_grouping_count = (
            db.query(GroupingCamper)
            .filter(GroupingCamper.grouping_camp_id == grouping_camp_id)
            .count()
        )
        grouping_camp_capacity = (
            db.query(GroupingCamp.maximum_capacity)
            .filter(GroupingCamp.id == grouping_camp_id)
            .first()
        )
        if actual_grouping_count >= grouping_camp_capacity:
            grouping_camper_create = GroupingCamperCreate(
                camper_id=camper, grouping_camp_id=grouping_camp_id
            )
            create_new_grouping_camper(db, grouping_camper_create)
        else:
            return {"status":"Capacidad llena"}
    return {"status": "success"}


def update_grouping_camper(
    db: Session, grouping_camper_id: int, update_data: GroupingCamperUpdate
):
    db.query(GroupingCamper).filter(GroupingCamper.id == grouping_camper_id).update(
        update_data.dict()
    )
    db.commit()
    return (
        db.query(GroupingCamper).filter(GroupingCamper.id == grouping_camper_id).first()
    )
def available_campers_to_add_in_grouping(grouping_camp_id: int, db: Session):
    grouping_camp = db.query(GroupingCamp).filter(GroupingCamp.id == grouping_camp_id).first();
    if grouping_camp == None:
        raise HTTPException(status_code=404, detail="Grouping camp not found")  
    

    query = db.query(
        Camper.id,
        (Camper.name + ' ' + Camper.lastname_father + ' ' + Camper.lastname_mother).label('name'),
        Camper.birthday,
        Constant.value.label('gender')
    ).join(
        CamperInCamp, CamperInCamp.camper_id == Camper.id
    ).join(
        Constant, Camper.gender_id == Constant.id
    ).filter(
        CamperInCamp.camp_id == grouping_camp.camp_id,
            ~Camper.id.in_(
                db.query(GroupingCamper.camper_id).filter(
                    GroupingCamper.grouping_camp_id == grouping_camp_id
            )
        )
    ).order_by(Camper.id)
    
    data = db.execute(query)
    return data.mappings().all()