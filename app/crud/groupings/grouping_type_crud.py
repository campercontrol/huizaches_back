from sqlalchemy.orm import Session
from model.groupings.grouping_type import GroupingType
from schema.groupings.grouping_type_schema import GroupingTypeCreate, GroupingTypeUpdate

def get_all_grouping_types(db: Session):
    return db.query(GroupingType).all()

def get_grouping_type_by_id(db: Session, grouping_type_id: int):
    return db.query(GroupingType).filter(GroupingType.id == grouping_type_id).first()

def create_new_grouping_type(db: Session, grouping_type_data: GroupingTypeCreate):
    db_grouping_type = GroupingType(**grouping_type_data.dict())
    db.add(db_grouping_type)
    db.commit()
    db.refresh(db_grouping_type)
    return db_grouping_type

def update_grouping_type(db: Session, grouping_type_id: int, update_data: GroupingTypeUpdate):
    db.query(GroupingType).filter(GroupingType.id == grouping_type_id).update(update_data.dict())
    db.commit()
    return db.query(GroupingType).filter(GroupingType.id == grouping_type_id).first()


def delete_grouping_type(db: Session, grouping_type_id: int):
    grouping_type_to_delete = db.query(GroupingType).filter(GroupingType.id == grouping_type_id).first()
    if grouping_type_to_delete:
        db.delete(grouping_type_to_delete)
        db.commit()
        return True
    return False
