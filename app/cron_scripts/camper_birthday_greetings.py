# birthday_greetings.py
import os
from sqlalchemy import text, desc, and_, or_, func, extract
from sqlalchemy.orm import Session
from fastapi import Depends
from utils.db import SessionLocal
from model.campers.camper import Camper
from model.camps.camper_in_camp import CamperInCamp
from model.camps.camp import Camp
from model.campers import Parent
from model.user import User
from datetime import date
from helper.mailing_helpers import send_mail_template, get_admin_users_for_mailing

BIRTHDAY_CAMPER_IS_IN_CAMP_PARENT_TEMPLATE_ID = int(os.getenv("BIRTHDAY_CAMPER_IS_IN_CAMP_PARENT_TEMPLATE_ID"))
BIRTHDAY_CAMPER_UPCOMING_CAMP_PARENT_TEMPLATE_ID = int(os.getenv("BIRTHDAY_CAMPER_UPCOMING_CAMP_PARENT_TEMPLATE_ID"))
BIRTHDAY_CAMPER_PAST_CAMP_PARENT_TEMPLATE_ID = int(os.getenv("BIRTHDAY_CAMPER_PAST_CAMP_PARENT_TEMPLATE_ID"))
BIRTHDAY_CAMPER_IS_IN_CAMP_ADMIN_TEMPLATE_ID = int(os.getenv("BIRTHDAY_CAMPER_IS_IN_CAMP_ADMIN_TEMPLATE_ID"))
BIRTHDAY_CAMPER_UPCOMING_CAMP_ADMIN_TEMPLATE_ID = int(os.getenv("BIRTHDAY_CAMPER_UPCOMING_CAMP_ADMIN_TEMPLATE_ID"))
BIRTHDAY_CAMPER_PAST_CAMP_ADMIN_TEMPLATE_ID = int(os.getenv("BIRTHDAY_CAMPER_PAST_CAMP_ADMIN_TEMPLATE_ID"))
CAMP_STATUS_ENROLLED_ID = int(os.getenv("CAMP_STATUS_ENROLLED_ID"))

def main():
    print("===============BIRTHDAY SCRIPT IS EXECUTING===============")
    db = SessionLocal()
    
    admin_users = get_admin_users_for_mailing(db)
    
    today = date.today()
    print("===============QUERYING THE DATABASE FOR CAMPER BIRTHDAYS===============")
    birthday_campers = (db.query(Camper, Parent, User).select_from(Camper)
                        .join(Parent, Parent.id == Camper.parent_id)
                        .join(User, User.id == Parent.user_id)
                        .filter(extract('month', Camper.birthday) == extract('month', func.current_date()), extract('day', Camper.birthday) == extract('day', func.current_date())).all())

    if birthday_campers:
        print("===============THERE ARE CAMPERS CELEBRATING THEIR BIRTHDAYS===============")
        print("===============SENDING EMAILS...===============")
        for camper in birthday_campers:
            try:
                camper_camps = (
                    db.query(CamperInCamp, Camp)
                    .select_from(CamperInCamp)
                    .join(Camp, Camp.id == CamperInCamp.camp_id)
                    .filter(
                        CamperInCamp.camper_id == camper[0].id,
                        CamperInCamp.status == CAMP_STATUS_ENROLLED_ID,  # enrolled
                    )
                    .order_by(desc(Camp.created_at))
                    .all()
                )

                current_camp = next(
                    ((cic, camp) for cic, camp in camper_camps if camp.start.date() <= today and today <= camp.end.date()),
                    None
                )
                forthcoming_camp = next(
                    ((cic, camp) for cic, camp in camper_camps if camp.start.date() > today),
                    None
                )
                past_camp = next(
                    ((cic, camp) for cic, camp in camper_camps if camp.end.date() < today),
                    None
                )
                tutor_1_context = {
                    "name": camper[1].tutor_name,
                    "lastname_father": camper[1].tutor_lastname_father,
                    "lastname_mother": camper[1].tutor_lastname_mother,
                    "email": camper[2].email
                }
                tutor_2_context = {
                    "name": camper[1].contact_name,
                    "lastname_father": camper[1].contact_lastname_father,
                    "lastname_mother": camper[1].contact_lastname_mother,
                    "email": camper[1].contact_email
                }
                
                context = {
                            "camper": camper[0],
                            "user": tutor_1_context
                } 
                if current_camp:
                    context["camp"] = current_camp[1]
                    send_mail_template(db, camper[2].email, BIRTHDAY_CAMPER_IS_IN_CAMP_PARENT_TEMPLATE_ID, context)
                    # send mail to second tutor
                    context["user"] = tutor_2_context
                    send_mail_template(db, tutor_2_context["email"], BIRTHDAY_CAMPER_IS_IN_CAMP_PARENT_TEMPLATE_ID, context)
                    
                    
                    for admin_user in admin_users:
                        context["user"] = admin_user
                        send_mail_template(db, [admin_user.email], BIRTHDAY_CAMPER_IS_IN_CAMP_ADMIN_TEMPLATE_ID, context)
                    
                elif forthcoming_camp:
                    context["camp"] = forthcoming_camp[1]
                    context["user"] = tutor_1_context
                    send_mail_template(db, camper[2].email, BIRTHDAY_CAMPER_UPCOMING_CAMP_PARENT_TEMPLATE_ID, context)
                    # send mail to second tutor
                    context["user"] = tutor_2_context
                    send_mail_template(db, tutor_2_context["email"], BIRTHDAY_CAMPER_UPCOMING_CAMP_PARENT_TEMPLATE_ID, context)

                    for admin_user in admin_users:
                        context["user"] = admin_user
                        send_mail_template(db, [admin_user.email], BIRTHDAY_CAMPER_UPCOMING_CAMP_ADMIN_TEMPLATE_ID, context)

                elif past_camp:
                    context["camp"] = past_camp[1]
                    context["user"] = tutor_1_context
                    send_mail_template(db, camper[2].email, BIRTHDAY_CAMPER_PAST_CAMP_PARENT_TEMPLATE_ID, context)
                    
                    # send mail to second tutor
                    context["user"] = tutor_2_context
                    send_mail_template(db, tutor_2_context["email"], BIRTHDAY_CAMPER_PAST_CAMP_PARENT_TEMPLATE_ID, context)
                    
                    
                    for admin_user in admin_users:
                        context["user"] = admin_user
                        send_mail_template(db, [admin_user.email], BIRTHDAY_CAMPER_PAST_CAMP_ADMIN_TEMPLATE_ID, context)
                print(f"===============BIRTHDAY EMAILS SENT FOR CAMPER ID {camper[0].id}===============")
            except Exception as e:
                print(f"!!!!!!!!!!!!!!!AN ERROR OCURRED WHILE SENDIND BIRTHDAY EMAILS FOR CAMPER {camper[0].id}!!!!!!!!!!!!!!!")
                print(e)
        print("===============BIRTHDAY EMAILS SCRIPT EXECUTED===============")
    else:
        print("===============NO CAMPERS WITH BIRTHDAY TODAY, NOTHING TO SEND.===============")
if __name__ == "__main__":
    main()
