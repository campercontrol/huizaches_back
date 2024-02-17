from sqlalchemy import case, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from utils.db import db_mapping_rows_to_dict


def append_campers_for_parent_admin(db, parents):
    '''
        Recibe al tutor con los campos del admin y regresa el mismo tutor
        con su lista de campers que tiene dados de alta
    '''
    from model.campers import Parent
    from model.campers import Camper
    from crud.campers.camper_crud import get_campers_from_parent

    
    possible_parents= []
    parents = db_mapping_rows_to_dict(parents)
    for parent in parents:
        campers = get_campers_from_parent(db, parent.tutor_id)
        parent_modify= {
            "user_id": parent.user_id,
            "tutor_id": parent.tutor_id,
            "tutor_name": parent.tutor_name,
            "tutor_lastname_father": parent.tutor_lastname_father,
            "tutor_lastname_mother": parent.tutor_lastname_mother,
            "tutor_home_phone": parent.tutor_home_phone,
            "tutor_work_phone": parent.tutor_work_phone,
            "tutor_cellphone": parent.tutor_cellphone,
            "tutor_email": parent.tutor_email,
            "second_tutor_email": parent.second_tutor_email,
            "campers": campers
        }
            
        possible_parents.append(parent_modify)
    
    return possible_parents