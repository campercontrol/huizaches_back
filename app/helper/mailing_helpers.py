import os
from jinja2 import Environment, BaseLoader
from model.campers import Camper, Parent
from model.mailings import EmailTemplate
from model.user import User
from model.staffs import Staff
from sqlalchemy.orm import Session
from utils.email_tools import send_simple_message
from utils.db import db_mapping_rows_to_dict

PAYMENT_TABLE_TEMPLATE_ID = os.getenv("PAYMENT_TABLE_TEMPLATE_ID")


# from utils.functions_jwt import create_user_verify_url
# def send_mail_template(
#     db,
#     send_to: list[str],
#     template_id: int,
#     camper: Camper = None,
#     parent_id: int = None,
# ):
#     print("(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((")
#     print(parent_id)
#     if parent_id:
#         parent = db.query(Parent).filter_by(id=parent_id).first()

#     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#     print(parent)
#     context = {"user": parent}
#     template_content =  (
#         db.query(EmailTemplate.title, EmailTemplate.template).filter(EmailTemplate.id == template_id).first()
#     )
#     print("###############################################################3")
#     print(template_content[0])
#     template_env = Environment(loader=BaseLoader).from_string(str(template_content.template))
#     html_content = template_env.render(context)
#     send_simple_message(
#         "", send_to, template_content.title, html_content
#     )
#     return 1

def send_mail_parent(
    db,
    send_to: list[str],
    template_id: int,
    parent_user,
    parent_profile,
):
    # data = {
    #     "user_email": parent_profile.email
    # }
    # url = create_user_verify_url(data)
    context = {
        "username": parent_profile.tutor_name,
        "father_lastname": parent_profile.tutor_lastname_father
    }

    template_content =  (
        db.query(EmailTemplate.title, EmailTemplate.template).filter(EmailTemplate.id == template_id).first()
    )

    template_env = Environment(loader=BaseLoader).from_string(str(template_content.template))
    html_content = template_env.render(context)
    send_simple_message(
        "", send_to, template_content.title, html_content
    )
    return 1
# def send_mail_prospect(
#     db,
#     send_to: list[str],
#     template_id: int,
#     prospect_profile,
#     prospect_user
# ):

#     data = {
#         "user_email": prospect_user.email
#     }
#     url = create_user_verify_url(data)

#     context = {
#         "username": prospect_profile.name,
#         "verify_url": url
#     }

#     template_content =  (
#         db.query(EmailTemplate.title, EmailTemplate.template).filter(EmailTemplate.id == template_id).first()
#     )
#     template_env = Environment(loader=BaseLoader).from_string(str(template_content.template))
#     html_content = template_env.render(context)
#     send_simple_message(
#         "", send_to, template_content.title, html_content
#     )
#     return 1

def send_mail_template(
    db,
    send_to: str,
    template_id: int,
    context: dict
):

    try:    
        template_content =  (
            db.query(EmailTemplate.title, EmailTemplate.template).filter(EmailTemplate.id == template_id).first()
        )
        template_env = Environment(loader=BaseLoader).from_string(str(template_content.template))
        template_env_title = Environment(loader=BaseLoader).from_string(str(template_content.title))
        html_content_title = template_env_title.render(context)
        
        html_content = template_env.render(context)
        send_simple_message(
            "", send_to, html_content_title, html_content
        )
        return True
    except Exception as ex:
        print(ex)
        return False

    
def send_mail_template_medical_visit(
    db,
    send_to: str,
    template_id: int,
    context: dict,
    medical_visit_table_id: int
):
    try:    
        template_content =  (
            db.query(EmailTemplate.title, EmailTemplate.template).filter(EmailTemplate.id == template_id).first()
        )
        # Template de la tabla de la visita medica
        medical_table_content = (
            db.query(EmailTemplate.template).filter(EmailTemplate.id == medical_visit_table_id).first()
        )
        
        template_env = Environment(loader=BaseLoader).from_string(str(template_content.template))
        template_env_medical_table = Environment(loader=BaseLoader).from_string(str(medical_table_content.template))
        template_env_title = Environment(loader=BaseLoader).from_string(str(template_content.title))
        html_content_title = template_env_title.render(context)
        html_content_medical_table = template_env_medical_table.render(context)
        
        context["medical_visit"] = html_content_medical_table
            
        html_content = template_env.render(context)    
        
        send_simple_message("", send_to, html_content_title, html_content)
        return True
    except Exception as ex:
        print(ex)
        return False



def send_mail_template_payment(
    db,
    send_to: str,
    template_id: int,
    context: dict,
):
    try:    
        template_content =  (
            db.query(EmailTemplate.title, EmailTemplate.template).filter(EmailTemplate.id == template_id).first()
        )
        # Template de la tabla de pagos
        payment_table_content = (
            db.query(EmailTemplate.template).filter(EmailTemplate.id == PAYMENT_TABLE_TEMPLATE_ID).first()
        )
        
        template_env = Environment(loader=BaseLoader).from_string(str(template_content.template))
        template_env_payment_table = Environment(loader=BaseLoader).from_string(str(payment_table_content.template))
        template_env_title = Environment(loader=BaseLoader).from_string(str(template_content.title))
        html_content_title = template_env_title.render(context)
        html_content_payment_table = template_env_payment_table.render(context)
        
        context["show_table_balance"] = html_content_payment_table
            
        html_content = template_env.render(context)    
        
        send_simple_message("", send_to, html_content_title, html_content)
        return True
    except Exception as ex:
        print(ex)
        return False

 
 
def create_html_payment_table(
    db,
    context
):
    try:
        html_content_payment_table = ''
        # Template de la tabla de pagos
        payment_table_content = (
            db.query(EmailTemplate.template).filter(EmailTemplate.id == PAYMENT_TABLE_TEMPLATE_ID).first()
        )

        template_env_payment_table = Environment(loader=BaseLoader).from_string(str(payment_table_content.template))
        html_content_payment_table = template_env_payment_table.render(context)
        
        return html_content_payment_table

    except Exception as ex:
        print(ex)
        return html_content_payment_table
 
def send_mail_template_plain_text(
    db,
    send_to: str,
    template_content: str,
    subject: str,
    context: dict
):

    # template_content =  (
    #     db.query(EmailTemplate.title, EmailTemplate.template).filter(EmailTemplate.id == template_id).first()
    # )
    template_env = Environment(loader=BaseLoader).from_string(template_content)
    html_content = template_env.render(context)
    
    template_env_title = Environment(loader=BaseLoader).from_string(subject)
    html_content_title = template_env_title.render(context)
    
    
    try:    
        send_simple_message(
            "", send_to, html_content_title, html_content
        )
        return True
    except Exception as ex:
        print(ex)
        return False
    
def get_admin_users_for_mailing(db: Session):
    query = db.query(Staff.name,
                     Staff.id,
                     Staff.lastname_father,
                     Staff.lastname_mother,
                     User.email).join(User, User.id == Staff.login_id).filter(User.is_admin == True)
    data = db.execute(query)
    return data.mappings().all()