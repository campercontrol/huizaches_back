from sqlalchemy import case, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from model.role import Role
from model.user import User
from model.campers import Parent
from model.staffs import Staff
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
            User.is_active.label('is_active'),
            User.hashed_pass.label('password')

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

    user = (
        db.query(User.role_id)
        .filter_by(id = user_id)
        .first()
    )

    if user[0] == 1:
        profile_id = (
            db.query(Parent.id)
            .join(User, User.id == Parent.user_id)
            .filter( Parent.user_id == user_id)
            .first()
        )

    if user[0] == 2:
        profile_id = (
            db.query(Staff.id)
            .join(User, User.id == Staff.login_id)
            .filter( Staff.login_id == user_id)
            .first()
        )
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
        .update({"answer": hashed_pass})
    )
    db.commit()

    return 1
