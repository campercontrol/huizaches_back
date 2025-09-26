from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from model.groupings.grouping_camp import GroupingCamp
from model.groupings.grouping_camper import GroupingCamper
from model.groupings.grouping import Grouping
from model.groupings.grouping_type import GroupingType
from schema.groupings.grouping_camp_schema import GroupingCampCreate, GroupingCampUpdate

def get_all_grouping_camps(db: Session):
    return db.query(GroupingCamp).all()

def get_grouping_camp_by_id(db: Session, grouping_camp_id: int):
    return db.query(GroupingCamp).filter(GroupingCamp.id == grouping_camp_id).first()

def create_new_grouping_camp(db: Session, grouping_camp_data: GroupingCampCreate):
    db_grouping_camp = GroupingCamp(**grouping_camp_data.dict())
    db.add(db_grouping_camp)
    db.commit()
    return db_grouping_camp

def update_grouping_camp(db: Session, grouping_camp_id: int, update_data: GroupingCampUpdate):
    db.query(GroupingCamp).filter(GroupingCamp.id == grouping_camp_id).update(update_data.dict())
    db.commit()
    return db.query(GroupingCamp).filter(GroupingCamp.id == grouping_camp_id).first()

def get_camp_groupings_by_camp_id(db: Session, camp_id: int):
    # query = (
    #     db.query(
    #         GroupingCamp.id,
    #         Grouping.id.label('grouping_id'),
    #         Grouping.name.label('grouping'),
    #         GroupingType.name.label('type')
    #     )
    #     .join(GroupingCamp, GroupingCamp.grouping_id == Grouping.id)
    #     .join(GroupingType, Grouping.grouping_type_id == GroupingType.id)
    #     .filter(GroupingCamp.camp_id == camp_id)
    # )
    query = (
        db.query(
            GroupingCamp.id,
            Grouping.id.label('grouping_id'),
            Grouping.name.label('grouping'),
            GroupingType.name.label('type'),
            func.concat(func.count(GroupingCamper.id), '/', GroupingCamp.maximum_capacity).label('capacity')            
        )
        .join(GroupingCamp, GroupingCamp.grouping_id == Grouping.id)
        .join(GroupingType, Grouping.grouping_type_id == GroupingType.id)
        .outerjoin(GroupingCamper, GroupingCamp.id == GroupingCamper.grouping_camp_id)
        .filter(GroupingCamp.camp_id == camp_id)
        .group_by(
            Grouping.id,
            GroupingCamp.id,
            Grouping.name,
            GroupingType.name
        )
    )
    data = db.execute(query)
    return data.mappings().all()

def get_camper_groupings_by_camper_id_and_camp_id(db: Session, camper_id: int, camp_id: int):
        groupings_query = (
            db.query(Grouping.name, Grouping.id, Grouping.is_active, Grouping.grouping_type_id).select_from(GroupingCamper)
            .join(GroupingCamp, GroupingCamper.grouping_camp_id == GroupingCamp.id)
            .join(Grouping, Grouping.id == GroupingCamp.grouping_id)
            .filter(and_(GroupingCamper.camper_id == camper_id, GroupingCamp.camp_id == camp_id))
        )
        groupings = db.execute(groupings_query)
        groupings = groupings.mappings().all()
        
        return groupings