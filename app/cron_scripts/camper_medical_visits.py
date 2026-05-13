import os
from crud.campers.parent_crud import get_parent_by_camper_id, get_second_tutor_by_camper_id
from crud.mailings.mailing_crud import get_camp_info_by_id_mailing, get_camper_info_mailing
from crud.medical.camper_visit_crud import MEDICAL_VISIT_PARENT_TABLE_TEMPLATE_ID, MEDICAL_VISIT_PARENT_TEMPLATE
from sqlalchemy import text, desc, and_, or_, func, extract
from sqlalchemy.orm import Session
from fastapi import Depends
from utils.db import SessionLocal
from helper.mailing_helpers import send_mail_template, get_admin_users_for_mailing, send_mail_template_medical_visit
from datetime import date
from model.medical.medical_camper_visit import MedicalCamperVisit




def main():
    db = SessionLocal()
   
    medical_visits = (db.query(MedicalCamperVisit).filter(
        extract('month', MedicalCamperVisit.created_at) == extract('month', func.current_date()),
        extract('day', MedicalCamperVisit.created_at) == extract('day', func.current_date()),
        extract('year', MedicalCamperVisit.created_at) == extract('year', func.current_date())
    ).all())

   
    if medical_visits:
        print("===============THERE ARE MEDICAL VISITS CREATED TODAY===============")
        print("===============SENDING EMAILS...===============")
        for visit in medical_visits:
            try:
                first_parent = get_parent_by_camper_id(db, visit.camper_id)
                second_parent = get_second_tutor_by_camper_id(db, visit.camper_id)
                camper_data = get_camper_info_mailing(db, visit.camper_id)
                camp_data = get_camp_info_by_id_mailing(db, visit.camp_id)
 
 
                # Send email to the parents               
                first_parent_context = {
                "camper": camper_data,
                "user": first_parent,
                "camp": camp_data,
                "medical_visit": visit,
                "additional_photo": visit.additional_photo
                }
                second_parent_context = {
                    "camper": camper_data,
                    "user": second_parent,
                    "camp": camp_data,
                    "medical_visit": visit,
                    "additional_photo": visit.additional_photo
                }
                send_mail_template_medical_visit(db, first_parent["email"], MEDICAL_VISIT_PARENT_TEMPLATE, first_parent_context, MEDICAL_VISIT_PARENT_TABLE_TEMPLATE_ID)    
                send_mail_template_medical_visit(db, second_parent["email"], MEDICAL_VISIT_PARENT_TEMPLATE, second_parent_context, MEDICAL_VISIT_PARENT_TABLE_TEMPLATE_ID)    
                print(f"Email sent for medical visit ID {visit.id}")
            except Exception as e:
                print(f"Error sending email for medical visit ID {visit.id}: {e}")    
    else:
        print("===============NO MEDICAL VISITS CREATED TODAY===============")
        
   
   
   
   


if __name__ == "__main__":
    main()
