# birthday_greetings.py
import os
from sqlalchemy import text, desc, and_, or_, func
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
                        .filter(func.date(Camper.birthday) == today).all())

    if birthday_campers:
        print("===============THERE ARE CAMPERS CELEBRATING THEIR BIRTHDAYS===============")
        for camper in birthday_campers:
            try:
                print("===============SENDING EMAILS...===============")
                camper_camps = (
                    db.query(CamperInCamp, Camp)
                    .join(Camp, Camp.id == CamperInCamp.camp_id)
                    .filter(
                        CamperInCamp.camper_id == camper[0].id,
                        CamperInCamp.status == CAMP_STATUS_ENROLLED_ID,  # enrolled
                    )
                    .order_by(desc(Camp.created_at))
                    .all()
                )

                current_camp = next(
                    ((cic, camp) for cic, camp in camper_camps if camp.start.date() <= today <= camp.end.date()),
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
                
                context = {
                            "camper": camper[0],
                            "user": camper[1],

                    } 
                if current_camp:
                    context["camp"] = current_camp[1]
                    send_mail_template(db, camper[2].email, BIRTHDAY_CAMPER_IS_IN_CAMP_PARENT_TEMPLATE_ID, context)
                    for admin_user in admin_users:
                        context["user"] = admin_user
                        send_mail_template(db, [admin_user.email], BIRTHDAY_CAMPER_IS_IN_CAMP_ADMIN_TEMPLATE_ID, context)
                    
                elif forthcoming_camp:
                    context["camp"] = forthcoming_camp[1]
                    send_mail_template(db, camper[2].email, BIRTHDAY_CAMPER_UPCOMING_CAMP_PARENT_TEMPLATE_ID, context)
                    for admin_user in admin_users:
                        context["user"] = admin_user
                        send_mail_template(db, [admin_user.email], BIRTHDAY_CAMPER_UPCOMING_CAMP_ADMIN_TEMPLATE_ID, context)

                elif past_camp:
                    context["camp"] = past_camp[1]
                    send_mail_template(db, camper[2].email, BIRTHDAY_CAMPER_PAST_CAMP_PARENT_TEMPLATE_ID, context)
                    for admin_user in admin_users:
                        context["user"] = admin_user
                        send_mail_template(db, [admin_user.email], BIRTHDAY_CAMPER_PAST_CAMP_ADMIN_TEMPLATE_ID, context)

                print("===============BIRTHDAY EMAILS SENT SUCCESSFULLY!===============")
                return {"status": 1, "msg": "Birthday emails sent successfully!"}
            except Exception as e:
                print(e)
                print("!!!!!!!!!!!!!!!AN ERROR OCURRED WHILE SENDIND BIRTHDAY EMAILS!!!!!!!!!!!!!!!")
                return {"status": 3, "msg": "Internal Server Error"}
    else:
        print("===============NO CAMPERS WITH BIRTHDAY TODAY, NOTHING TO SEND.===============")
        return {"status": 2, "msg": "No campers with birthday today, nothing to send."}
    
if __name__ == "__main__":
    main()
