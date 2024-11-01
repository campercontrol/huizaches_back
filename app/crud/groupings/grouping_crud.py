from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from model.groupings.grouping_type import GroupingType
from model.groupings.grouping import Grouping
from schema.groupings.grouping_schema import GroupingCreate, GroupingUpdate


def get_all_groupings(db: Session):
    query = db.query(Grouping.id, Grouping.name, Grouping.is_active, GroupingType.id.label('grouping_type_id'), GroupingType.name.label('grouping_type_name')).join(GroupingType, GroupingType.id == Grouping.grouping_type_id).order_by(Grouping.id)
    groupings = db.execute(query)
    groupings = groupings.mappings().all()
    return groupings



def get_grouping_by_id(db: Session, grouping_id: int):
    return db.query(Grouping).filter(Grouping.id == grouping_id).first()


def create_new_grouping(db: Session, grouping_data: GroupingCreate):
    db_grouping = Grouping(**grouping_data.dict())
    try:
        db.add(db_grouping)
        db.commit()
        db.refresh(db_grouping)
        return db_grouping
    except SQLAlchemyError as e:
        print(e)
        return None


def update_grouping(db: Session, grouping_id: int, update_data: GroupingUpdate):
    grouping = db.query(Grouping).filter_by(id=grouping_id).one_or_none()
    if grouping == None:
        raise HTTPException(status_code=404, detail="Grouping not found")
    try:
        updated_grouping = (
            db.query(Grouping)
            .filter_by(id=grouping_id)
            .update(update_data, synchronize_session="fetch")
        )
        db.commit()
    except Exception as ex:
        print(ex)
        return {"status": 3, "msg": "Internal Server Error"}
    
    return {"status": 1, "msg": "Season updated successfully"}

def delete_grouping(db: Session, grouping_id: int):
    grouping_to_delete = db.query(Grouping).filter(Grouping.id == grouping_id).first()
    if grouping_to_delete:
        db.delete(grouping_to_delete)
        db.commit()
        return True
    return False

