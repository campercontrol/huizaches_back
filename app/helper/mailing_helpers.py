from jinja2 import Environment, BaseLoader
from model.campers import Camper, Parent
from model.mailings import EmailTemplate

from utils.email_tools import send_simple_message
from utils.db import db_mapping_rows_to_dict
from utils.functions_jwt import create_user_verify_url
def send_mail_template(
    db,
    send_to: list[str],
    template_id: int,
    camper: Camper = None,
    parent_id: int = None,
):
    print("(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((")
    print(parent_id)
    if parent_id:
        parent = db.query(Parent).filter_by(id=parent_id).first()

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(parent)
    context = {"user": parent}
    template_content =  (
        db.query(EmailTemplate.title, EmailTemplate.template).filter(EmailTemplate.id == template_id).first()
    )
    print("###############################################################3")
    print(template_content[0])
    template_env = Environment(loader=BaseLoader).from_string(str(template_content.template))
    html_content = template_env.render(context)
    send_simple_message(
        "", send_to, template_content.title, html_content
    )
    return 1

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

def send_mail_prospect(
    db,
    send_to: list[str],
    template_id: int,
    prospect_profile,
    prospect_user
):

    data = {
        "user_email": prospect_user.email
    }
    url = create_user_verify_url(data)

    context = {
        "username": prospect_profile.name,
        "verify_url": url
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
        html_content = template_env.render(context)
        send_simple_message(
            "", send_to, template_content.title, html_content
        )
        return True
    except Exception as ex:
        print(ex)
        return False
    
    
def send_mail_template_plain_text(
    db,
    send_to: str,
    template_id: int,
    template_content: str,
    subject: str,
    context: dict
):

    template_content =  (
        db.query(EmailTemplate.title, EmailTemplate.template).filter(EmailTemplate.id == template_id).first()
    )
    template_env = Environment(loader=BaseLoader).from_string(template_content)
    html_content = template_env.render(context)
    try:    
        send_simple_message(
            "", send_to, subject, html_content
        )
        return True
    except Exception as ex:
        print(ex)
        return False