from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from model.campers import CamperComment
from model.role import Role
from model.user import User
from model.staffs.staff import Staff
from model.campers.camper import Camper
from model.campers.parent import Parent
from model.campers.school import School
from model.medical.doctor import Doctor
from schema.campers.camper_comment_schema import (
    CamperCommentCreate,
    CamperCommentModify,
)
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case, and_


def get_all_camper_comment(db):
    rows = db.query(CamperComment).all()
    return rows


def get_camper_comment_by_id(db, camper_comment_id: int):
    return db.query(CamperComment).filter_by(id=camper_comment_id).first()


def create_new_camper_comment(db, new_camper_comment: CamperCommentCreate):
    try:
        db_camper_comment = CamperComment(**new_camper_comment.dict())
        db.add(db_camper_comment)
        db.commit()
        db.refresh(db_camper_comment)
    except SQLAlchemyError as alchemyError:
        db.rollback()
        print("#=================================#")
        print(alchemyError)
        print("#=================================#")
        return {"status": 3, "msg": "An error ocurred while saving"} 
    except Exception as ex:
        print(f"No se pudo guardar en la base de datos: {ex}")
        return {"status": 3, "msg": "An error ocurred while saving"}
    return {"status": 1, "msg": "Camper comment saved succesfully"}


def update_camper_comment_by_id(
    db, camper_comment_id: int, modify_camper_comment: CamperCommentModify
):
    rows_updated = (
        db.query(CamperCommentModify)
        .filter_by(id=camper_comment_id)
        .update(modify_camper_comment, synchronize_session="fetch")
    )
    db.commit()
    return rows_updated


def get_camper_comment_by_camper_for_parent(db, camper_id: int):
    rows = (
        db.query(CamperComment)
        .filter(
            and_(
                CamperComment.camper_id == camper_id,
                CamperComment.is_public == True,
                CamperComment.show_to == 2,
            )
        )
        .all()
    )
    return rows

def get_all_camper_comments(db, camper_id: int):
    parent_role = 1
    staff_role = 2
    school_role = 3
    doctor_role = 5    
    
    comments_query = (
        db.query(
            CamperComment.id,
            CamperComment.comment,
            CamperComment.camp_id,
            CamperComment.camper_id,
            CamperComment.is_public,
            CamperComment.show_to,
            CamperComment.user_id
        )
        .filter(
                CamperComment.camper_id == camper_id
        )
    )
    comments = db.execute(comments_query)
    comments = comments.mappings().all()
    camper_comments = []
    
    for comment in comments:
        comment_dict = dict(comment)
        user_id = comment["user_id"]
        user = (
        db.query(User)
        .filter(
            User.id == user_id
        ).first())    
        
        user_info = None
        
        if user.role_id == parent_role:
            user_info_query = (db.query(Parent.id, func.concat(Parent.tutor_name, ' ', Parent.tutor_lastname_father, ' ', Parent.tutor_lastname_mother).label('fullname'), Role.name.label("role")).select_from(Parent).join(User, User.id == Parent.user_id).join(Role, Role.id == User.role_id).filter(User.id == user.id))
            user_info = db.execute(user_info_query)
            user_info = user_info.mappings().first()
        if user.role_id == staff_role:
            user_info_query = (db.query(Staff.id, func.concat(Staff.name, ' ', Staff.lastname_father, ' ', Staff.lastname_mother).label('fullname'), Role.name.label("role"), Staff.coordinator).select_from(Staff).join(User, User.id == Staff.login_id).join(Role, Role.id == User.role_id).filter(User.id == user.id))
            user_info = db.execute(user_info_query)
            user_info = user_info.mappings().first()
        if user.role_id == school_role:
            user_info_query = (db.query(School.id, School.name.label('fullname'), Role.name.label("role")).select_from(School).join(User, User.id == School.login_id).join(Role, Role.id == User.role_id).filter(User.id == user.id))
            user_info = db.execute(user_info_query)
            user_info = user_info.mappings().first()
        if user.role_id == doctor_role:
            user_info_query = (db.query(Doctor.id,  func.concat(Doctor.name, ' ', Doctor.lastname_father, ' ', Doctor.lastname_mother).label('fullname'), Role.name.label("role")).select_from(Doctor).join(User, User.id == Doctor.login_id).join(Role, Role.id == User.role_id).filter(User.id == user.id))
            user_info = db.execute(user_info_query)
            user_info = user_info.mappings().first()
            
        comment_dict["comment_author"] = user_info
        camper_comments.append(comment_dict)

    return camper_comments


def get_camper_comment_by_camper_for_admin(db, camper_id: int):
    rows = (
        db.query(CamperComment)
        .filter(
            and_(
                CamperComment.camper_id == camper_id,
                CamperComment.is_public == True,
                CamperComment.show_to == 2,
            )
        )
        .all()
    )
    return rows
def get_camper_comment_by_camper_for_school(db, camper_id: int):
    rows = (
        db.query(CamperComment)
        .filter(
            and_(
                CamperComment.camper_id == camper_id,
                CamperComment.is_public == True,
                CamperComment.show_to == 3,
            )
        )
        .all()
    )
    return rows
