from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_
from model.groupings.grouping_camper import GroupingCamper
from model.groupings.grouping_camp import GroupingCamp
from model.groupings.grouping_type import GroupingType
from model.groupings.grouping import Grouping
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


def create_new_grouping_camper(db: Session, grouping_campers: GroupingCamperCreate):
    grouping_camp_id = grouping_campers[0].grouping_camp_id

    try:
        grouping_camp_row = (
            db.query(GroupingCamp.id.label('grouping_id'), GroupingCamp.camp_id, GroupingType.id.label('grouping_type_id'), GroupingCamp.maximum_capacity).select_from(GroupingCamp).filter(GroupingCamp.id == grouping_camp_id)
            .join(Grouping, Grouping.id == GroupingCamp.grouping_id)
            .join(GroupingType, GroupingType.id == Grouping.grouping_type_id)
            .first()
        )
        grouping_current_capacity = db.query(GroupingCamper).filter(GroupingCamper.grouping_camp_id == grouping_camp_id).count()

        if len(grouping_campers) + grouping_current_capacity > grouping_camp_row.maximum_capacity:
            return {"status": 2, "detail": "La cantidad de campers excede la capacidad de la agrupación"}
        
        for grouping_camper in grouping_campers:
            search_grouping_camper = (
                db.query(GroupingCamper).select_from(GroupingCamper)
                .filter(GroupingCamper.camper_id == grouping_camper.camper_id, GroupingCamper.grouping_camp_id == grouping_camp_id).first()
                )
            
            camper_info = db.query(Camper.id, Camper.name, Camper.lastname_father, Camper.lastname_mother).filter(Camper.id == grouping_camper.camper_id).first()
            camper_groupings = (
                db.query(GroupingType.id.label("grouping_type_id"), GroupingCamp.id).select_from(GroupingCamper)
                .join(GroupingCamp, GroupingCamp.id == GroupingCamper.grouping_camp_id)
                .join(Grouping, Grouping.id == GroupingCamp.grouping_id)
                .join(GroupingType, GroupingType.id == Grouping.grouping_type_id)                     
            ).where(and_(GroupingCamper.camper_id == grouping_camper.camper_id, GroupingCamp.camp_id == grouping_camp_row.camp_id)).all()
            
            if not search_grouping_camper == None:
                
                return {"status":3, "detail": "El camper " + camper_info.name + " " + camper_info.lastname_father + " " + camper_info.lastname_mother + ' ya se encuentra en la agrupación. No se añadieron los campers.'}

            for camper_grouping in camper_groupings:
                if camper_grouping.grouping_type_id == grouping_camp_row.grouping_type_id:
                    return {"status": 4, "detail": "El camper " + camper_info.name + " " + camper_info.lastname_father + " " + camper_info.lastname_mother + " ya se encuentra en una agrupación del mismo tipo, no es posible agregar."}
            
            new_grouping_camper = GroupingCamper(**grouping_camper.dict())
            db.add(new_grouping_camper)
        db.commit()
    except Exception as ex:
        print(ex)
        db.rollback()
        raise HTTPException(status_code=500, detail="Ocurrio un error, los campers no se añadieron correctamente")
    
    return {"status": 1, "detail": "Se han añadido correctamente los campers a la agrupación"}
    

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
        
    catalog_one = aliased(Constant)
    catalog_two = aliased(Constant)
    
    query = db.query(
        Camper.id,
        (Camper.name + ' ' + Camper.lastname_father + ' ' + Camper.lastname_mother).label('name'),
        Camper.birthday,
        catalog_one.value.label('gender'),
        catalog_two.value.label('grade')
    ).join(
        CamperInCamp, CamperInCamp.camper_id == Camper.id
    ).join(
        catalog_one, Camper.gender_id == catalog_one.id
    ).join(
        catalog_two, Camper.grade == catalog_two.id
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