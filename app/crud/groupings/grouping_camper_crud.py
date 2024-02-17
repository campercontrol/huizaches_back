from sqlalchemy.orm import Session
from model.groupings.grouping_camper import GroupingCamper
from model.groupings.grouping_camp import GroupingCamp
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


def create_new_grouping_camper(db: Session, grouping_camper_data: GroupingCamperCreate):
    db_grouping_camper = GroupingCamper(**grouping_camper_data.dict())
    db.add(db_grouping_camper)
    db.commit()
    db.refresh(db_grouping_camper)
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
