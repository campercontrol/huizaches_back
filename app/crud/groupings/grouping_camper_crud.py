from sqlalchemy.orm import Session, aliased
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


def create_new_grouping_camper(db: Session, grouping_campers: GroupingCamperCreate):
    db.begin()
    grouping_camp_id = grouping_campers[0].grouping_camp_id

    try:
        grouping_camp_row = db.query(GroupingCamp).filter(GroupingCamp.id == grouping_camp_id).first()
        grouping_current_capacity = db.query(GroupingCamper).filter(GroupingCamper.grouping_camp_id == grouping_camp_id).count()

        if len(grouping_campers) + grouping_current_capacity > grouping_camp_row.maximum_capacity:
            return {"detail": "La cantidad de campers excede la capacidad de la agrupación"}

        if grouping_camp_row == None:
            return {"detail": "No se econtró el grouping_camp_id"}        

        for grouping_camper in grouping_campers:
            search_grouping_camper = db.query(GroupingCamper).filter(GroupingCamper.camper_id == grouping_camper.camper_id, GroupingCamper.grouping_camp_id == grouping_camp_id).first()        
            if not search_grouping_camper == None:
                return {"detail": "El camper " + str(search_grouping_camper.camper_id) + ' ya se encuentra en la agrupación. No se añadieron los campers'}
            new_grouping_camper = GroupingCamper(**grouping_camper.dict())
            db.add(new_grouping_camper)
        db.commit()
    except Exception as ex:
        print(ex)
        db.rollback()
        raise HTTPException(status_code=500, detail="Ocurrio un error, los campers no se añadieron correctamente")
    
    db.close()
    return {"detail": "Se han añadido correctamente los campers a la agrupación"}
    

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