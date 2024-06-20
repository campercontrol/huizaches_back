from sqlalchemy import case, or_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import delete
from model.role import Role
from model.user import User
from model.campers import School
from model.campers import Camper
from model.campers import Parent
from model.staffs import Staff
from model.staffs import StaffVaccine
from model.staffs import StaffComment
from model.staffs import StaffFoodRestriction
from model.trainings import StaffInTraining
from model.camps import StaffInCamp
from model.mailings import StaffCampaign
from model.medical import Doctor
from model.medical import MedicalStaffVisit
from model.trophies import TrophyStaff
from model.payments import Payment
from model.mailings import SchoolCampaign
from model.camps import Camp

from utils.hash import hash_str
from utils.db import db_mapping_rows_to_dict


def get_all_user(db, is_active):
    rows = (
        db.query(
            User.id.label('id'),
            User.email.label('email'),
            User.hashed_pass.label('hashed_pass'),
            User.role_id.label('role_id'),
            Role.name.label('role_name'),
            User.is_admin,
            User.is_superuser.label('is_superuser'),
            User.is_active.label('is_active'),
        )
        .join(
            Role, Role.id == User.role_id
        ).filter(
            User.is_active == is_active,
        )
        .all()
    )

    return db_mapping_rows_to_dict(rows)

def get_users_all_info(db, user_id):
    query = db.query(
        User.id,
        User.email,
        Parent.tutor_name,
        Parent.tutor_lastname_father,
        Parent.tutor_lastname_mother
    ).join(Parent, User.id == Parent.user_id).filter(User.id == user_id)
    data = db.execute(query)
    parent = data.mappings().first()
    print(parent)
    
    

def create_new_user(db, new_user):
    db_user = None
    try:
        db_user = User(
            email=new_user.email,
            hashed_pass=hash_str(new_user.passw),
            role_id=new_user.role_id,
            is_superuser=new_user.is_superuser                
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_user = None
        return db_user
    except Exception as ex:
        db_user = None
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_user


def create_new_prospect_user(db, new_user):
    db_user = None
    try:
        db_user = User(
            email=new_user.email,
            hashed_pass=hash_str(new_user.passw),
            role_id= 2,
            is_active= False,
            is_coordinator = False,
            is_admin = False,
            is_employee = False,
            is_superuser = False           
                 
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as e:
        print("#=================")
        print(e)
        print("#=================")
        db_user = None
        return db_user
    except Exception as ex:
        db_user = None
        print(f"No se pudo guardar en la base de datos: {ex}")
    return db_user



def get_user_by_uuid(db, user_id):
    rows = []
    first_row = (
        db.query(
            User.email.label('email'),
            User.hashed_pass.label('hashed_pass'),
            User.role_id.label('role_id'),
            Role.name.label('role_name'),
            User.is_superuser.label('is_superuser'),
            User.is_active.label('is_active')

        )
        .join(
            Role, Role.id == User.role_id
        ).filter(
            User.id == user_id,
        )
        .first()
    )
    rows.append(first_row)

    return db_mapping_rows_to_dict(rows)


def crud_update_user_by_uuid(db, user_id, update_data):

    print(f"user_id:{user_id}")
    print(f"update_data:{update_data}")

    rows_updated = db.query(
    User
    ).filter_by(
        id = user_id,
    ).update(
        update_data,
        synchronize_session="fetch",
    )
    db.commit()
    print(f"rows_updated:{rows_updated}")
    return rows_updated

def crud_update_user_by_email(db, email, update_data):

    print(f"email:{email}")
    print(f"update_data:{update_data}")

    rows_updated = db.query(
    User
    ).filter_by(
        email = email,
    ).update(
        update_data,
        synchronize_session="fetch",
    )
    db.commit()
    print(f"rows_updated:{rows_updated}")
    return rows_updated

# ==========Login
def get_user_by_email(db, email):
    return db.query(User).filter_by(email=email).first()

def get_profile_id_by_user_id(db, user_id:int ):

    profile_id = ['']
    parent_role = 1
    staff_role = 2
    school_role = 3
    doctor_role = 5
    user_role = (
        db.query(User.role_id)
        .filter_by(id = user_id)
        .first()
    )
    # print("get profile ===============")
    # print(user_role[0])
    
    if user_role[0] == parent_role:
        profile_id = (
            db.query(Parent.id)
            .join(User, User.id == Parent.user_id)
            .filter( Parent.user_id == user_id)
            .first()
        )

    if user_role[0] == staff_role:
        profile_id = (
            db.query(Staff.id)
            .join(User, User.id == Staff.login_id)
            .filter( Staff.login_id == user_id)
            .first()
        )
    if user_role[0] == school_role:
        profile_id = (
            db.query(School.id)
            .join(User, User.id == School.login_id)
            .filter(Staff.login_id == user_id)
            .first()
        )
    if user_role[0] == doctor_role:
        profile_id = (
            db.query(Doctor.id)
            .join(User, User.id == Doctor.login_id)
            .filter(Doctor.login_id == user_id)
            .first()
        )
    # print(profile_id[0])
    return profile_id[0]

def search_user_by_email(db: Session, search: str):
    users = (
        db.query(
            User.id.label("user_id"),
            User.email.label("tutor_email"),
            User.is_active.label("user_active"),
            User.is_superuser.label("user_superuser"),
            User.is_employee.label("user_employee"),
            User.is_coordinator.label("user_coordinator"),
            User.is_admin.label("user_admin"),
            User.created_at.label("user_created")
        )        
        .filter(
            User.email.ilike(r"%{}%".format(search))
        )
        .all()
    )
    if users:
        return db_mapping_rows_to_dict(users)
    else:
        return "Data not found"

def update_password_all_users(db, hashed_pass:str):
    users= (
        db.query(
            User
        )
        .all()
    )
    for user in users:
        user.hashed_pass = hashed_pass

    db.commit()

    # "$2b$12$9QchmEH2rcRnHlfBnGe7ZunGbonntZc/RX2NHgClT7YSiakHRy.Pm"
    return 1

def update_user_by_id(db: Session, user_id:int, user_data):
    
    print(user_data)
    # if user_data['hashed_pass']:
    # user_data['hashed_pass'] = hash_str(user_data['hashed_pass'])
    

    try:
        user_to_update = db.query(User).filter_by(id=user_id).one()
        
        if user_data['hashed_pass'] != None:
            user_to_update.hashed_pass = hash_str(user_data['hashed_pass'])
        if user_data['role_id'] != None:
            user_to_update.role_id = user_data['role_id']
        if user_data['is_admin'] != None:
            user_to_update.is_admin = user_data['is_admin']
        if user_data['is_superuser'] != None:
            user_to_update.is_superuser = user_data['is_superuser']
        if user_data['is_coordinator'] != None:
            user_to_update.is_coordinator = user_data['is_coordinator']
        if user_data['is_employee'] != None:
            user_to_update.is_employee = user_data['is_employee'] 
        if user_data['is_active'] != None:
            user_to_update.is_active = user_data['is_active']       
        if user_data['email'] != None:
            user_to_update.email = user_data['email']
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        print(e)
        return {"status": 3, "msg": "Internal server error"}
    return {"status": 1, "msg": "User updated successfully"}


def delete_user_by_id(db: Session, user_id:int):
    user = db.query(User).filter(User.id==user_id).first()
    
    parent_role = 1
    staff_role = 2
    school_role = 3
    teacher_role = 4
    doctor_role = 5
    
    if user.role_id == parent_role:
        try:
            parent_user = db.query(Parent).filter(Parent.user_id == user.id).first()
            stmt_delete_parent_payment = delete(Payment).where(Payment.parent_id == parent_user.id) 
            stmt_delete_parent_campers = delete(Camper).where(Camper.parent_id == parent_user.id)
            stmt_delete_parent_user = delete(Parent).where(Parent.id == parent_user.id)
            stmt_delete_user = delete(User).where(User.id == user.id)
            db.execute(stmt_delete_parent_payment)
            db.execute(stmt_delete_parent_campers)
            db.execute(stmt_delete_parent_user)
            db.execute(stmt_delete_user)
            db.commit()
        except IntegrityError as IntegrityEx:
            db.rollback()
            print(IntegrityEx)
            return {"status": 2, "msg": "Can not delete Parent user, referenced by other table"}
        except Exception as ex:
            db.rollback()
            print(ex)
            return {"status": 3, "msg": "An unknown error ocurred while deleting"}
        return {"status": 1, "msg": "Parent user succesfully deleted"}
        
    if user.role_id == staff_role:
        try:
            staff_user = db.query(Staff).filter(Staff.login_id == user.id).first()
            stmt_delete_staff_vaccines = delete(StaffVaccine).where(StaffVaccine.staff_id == staff_user.id) 
            stmt_delete_staff_food_restriction = delete(StaffFoodRestriction).where(StaffFoodRestriction.staff_id == staff_user.id)
            stmt_delete_staff_comment = delete(StaffComment).where(StaffComment.staff_id == staff_user.id)
            stmt_delete_staff_in_training = delete(StaffInTraining).where(StaffInTraining.staff_id == staff_user.id)
            stmt_delete_staff_in_camps = delete(StaffInCamp).where(StaffInCamp.staff_id == staff_user.id)
            stmt_delete_staff_medical_visit = delete(MedicalStaffVisit).where(MedicalStaffVisit.staff_id == staff_user.id)
            stmt_delete_staff_trophy = delete(TrophyStaff).where(TrophyStaff.staff_id == staff_user.id)
            stmt_delete_staff_campaign = delete(StaffCampaign).where(StaffCampaign.staff_id == staff_user.id)
            stmt_delete_staff_user = delete(Staff).where(Staff.id == staff_user.id)
            
            stmt_delete_user = delete(User).where(User.id == user.id)
            db.execute(stmt_delete_staff_vaccines)
            db.execute(stmt_delete_staff_food_restriction)
            db.execute(stmt_delete_staff_comment)
            db.execute(stmt_delete_staff_in_training)
            db.execute(stmt_delete_staff_in_camps)
            db.execute(stmt_delete_staff_medical_visit)
            db.execute(stmt_delete_staff_trophy)
            db.execute(stmt_delete_staff_campaign)
            db.execute(stmt_delete_staff_user)
            db.execute(stmt_delete_user)
            db.commit()
        except IntegrityError as IntegrityEx:
            db.rollback()
            print(IntegrityEx)
            return {"status": 2, "msg": "Can not staff user, Staff user referenced by other table"}
        except Exception as ex:
            # db.rollback()
            print(ex)
            return {"status": 3, "msg": "An unknown error ocurred while deleting"}
        return {"status": 1, "msg": "Staff user succesfully deleted"}
        
    if user.role_id == school_role:
        try: 
            school_user = db.query(School).filter(School.login_id == user.id).first()
            stmt_delete_school_email_campaign = delete(SchoolCampaign).where(SchoolCampaign.school_id == school_user.id)
            stmt_delete_camp_school = delete(Camp).where(Camp.school_id == school_user.id)
            stmt_delete_school_user = delete(School).where(School.id == school_user.id)
            stmt_delete_user = delete(User).where(User.id == user.id)
            db.execute(stmt_delete_school_email_campaign)
            db.execute(stmt_delete_camp_school)
            db.execute(stmt_delete_school_user)
            db.execute(stmt_delete_user)
            db.commit()
        except IntegrityError as IntegrityEx:
            db.rollback()
            print(IntegrityEx)
            return {"status": 2, "msg": "Can not delete School user, School referenced by camps camp"}
        except Exception as ex:
            return {"status": 3, "msg": "An unknown error ocurred while deleting"}
        return {"status": 1, "msg": "School user succesfully deleted"}
    
    if user.role_id == school_role:
        try:
            medical_user = db.query(Doctor).filter(Doctor.login_id == user.id).first()
            stmt_delete_medical_user = delete(School).where(School.id == school_user.id)
            stmt_delete_user = delete(User).where(User.id == user.id)
            db.execute(stmt_delete_medical_user)
            db.execute(stmt_delete_user)
            db.commit()
        except IntegrityError as IntegrityEx:
            db.rollback()
            print(IntegrityEx)
            return {"status": 2, "msg": "Can not delete Medical user, referenced by other table"}
        except Exception as ex:
            return {"status": 3, "msg": "An unknown error ocurred while deleting"}
        return {"status": 1, "msg": "Medical user succesfully deleted"}