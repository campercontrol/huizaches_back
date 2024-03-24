from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from model.groupings.grouping import Grouping
from schema.groupings.grouping_schema import GroupingCreate, GroupingUpdate


def get_all_groupings(db: Session):
    return db.query(Grouping).order_by(Grouping.id).all()


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
    db.query(Grouping).filter(Grouping.id == grouping_id).update(update_data.dict())
    db.commit()
    return db.query(Grouping).filter(Grouping.id == grouping_id).first()


def delete_grouping(db: Session, grouping_id: int):
    grouping_to_delete = db.query(Grouping).filter(Grouping.id == grouping_id).first()
    if grouping_to_delete:
        db.delete(grouping_to_delete)
        db.commit()
        return True
    return False

