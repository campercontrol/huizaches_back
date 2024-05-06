from jinja2 import Environment, BaseLoader
from model.campers import Camper, Parent
from model.mailings import EmailTemplate

from utils.email_tools import send_simple_message
from utils.db import db_mapping_rows_to_dict


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


def send_mail_prospect(
    db,
    send_to: list[str],
    template_id: int,
    prospect_profile
):
    context = {"username": prospect_profile.name}

    template_content =  (
        db.query(EmailTemplate.title, EmailTemplate.template).filter(EmailTemplate.id == template_id).first()
    )
    # print(template_content[0])
    template_env = Environment(loader=BaseLoader).from_string(str(template_content.template))
    html_content = template_env.render(context)
    send_simple_message(
        "", send_to, template_content.title, html_content
    )
    return 1
