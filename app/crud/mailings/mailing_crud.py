from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from model.mailings import (
    Campaign,
    CamperCampaign,
    StaffCampaign,
    SchoolCampaign,
    EmailTemplate,
)
from model.campers import Camper, School
from model.staffs import Staff
from model.camps import Camp, Season
from model.trainings import Training, TrainingEvent
from schema.mailings.campaign_schema import CampaignCreate, CampaignModify
from utils.db import db_mapping_rows_to_dict
from sqlalchemy import case


def get_public_for_campaign(db, campaign_id: int):
    campers = (
        db.query(
            Camper.id,
            (
                Camper.name
                + " "
                + Camper.lastname_father
                + " "
                + Camper.lastname_mother
            ).label("camper_fullname")
        )
        .select_from(CamperCampaign)
        .join(Camper, Camper.id == CamperCampaign.camper_id)
        .filter(CamperCampaign.campaign_id == campaign_id)
        .distinct()
        .all()
    )

    staffs = (
        db.query(
            (
                Staff.name + " " + Staff.lastname_father + " " + Staff.lastname_mother
            ).label("staff_fullname")
        )
        .select_from(StaffCampaign)
        .join(Staff, Staff.id == StaffCampaign.staff_id)
        .filter(StaffCampaign.campaign_id == campaign_id)
        .distinct()
        .all()
    )

    school = (
        db.query(School.name)
        .select_from(SchoolCampaign)
        .join(School, School.id == SchoolCampaign.school_id)
        .filter(SchoolCampaign.campaign_id == campaign_id)
        .distinct()
        .all()
    )
    return {
        "campers": campers,
        "staffs": staffs,
        "school": school,
    }

def get_sent_camp(db, campaign_id: int):
    public_campaign = get_public_for_campaign(db, campaign_id)
    campaign = (
        db.query(
            Campaign.id.label("campaign_id"),
            Campaign.name.label("campaign_name"),
            Campaign.created_at.label("campaign_sent_date"),
            Camp.name.label("camp_name"),
            EmailTemplate.title.label("template_title"),
            EmailTemplate.template.label("template_body"),
        )
        .join(Camp, Camp.id == Campaign.camp_id)
        .join(EmailTemplate, EmailTemplate.id == Campaign.template_id)
        .filter(Campaign.id == campaign_id)
        .all()
    )
    return {
        "campers": public_campaign["campers"],
        "staffs": public_campaign["staffs"],
        "school": public_campaign["school"],
        "campaign_info": db_mapping_rows_to_dict(campaign)[0],
    }


def get_sent_camps(db, campaign_id: int):
    public_campaign = get_public_for_campaign(db, campaign_id)

    campaign = (
        db.query(
            Campaign.id.label("campaign_id"),
            Campaign.name.label("campaign_name"),
            Campaign.created_at.label("campaign_sent_date"),
            EmailTemplate.title.label("template_title"),
            EmailTemplate.template.label("template_body"),
        )
        .join(EmailTemplate, EmailTemplate.id == Campaign.template_id)
        .filter(Campaign.id == campaign_id)
        .all()
    )
    camps_unique = []
    camps_campers = (
        db.query(Camp.name)
        .select_from(CamperCampaign)
        .join(Camp, Camp.id == CamperCampaign.camp_id)
        .filter(CamperCampaign.campaign_id == campaign_id)
        .distinct()
        .all()
    )
    [
        camps_unique.append(camp_camper)
        for camp_camper in camps_campers
        if camp_camper not in camps_unique
    ]
    camps_staffs = (
        db.query(Camp.name)
        .select_from(StaffCampaign)
        .join(Camp, Camp.id == StaffCampaign.camp_id)
        .filter(StaffCampaign.campaign_id == campaign_id)
        .distinct()
        .all()
    )
    [
        camps_unique.append(camp_staff)
        for camp_staff in camps_staffs
        if camp_staff not in camps_unique
    ]
    camps_school = (
        db.query(Camp.name)
        .select_from(SchoolCampaign)
        .join(Camp, Camp.id == SchoolCampaign.camp_id)
        .filter(SchoolCampaign.campaign_id == campaign_id)
        .distinct()
        .all()
    )
    [
        camps_unique.append(camp_school)
        for camp_school in camps_school
        if camp_school not in camps_unique
    ]

    return {
        "campers": public_campaign["campers"],
        "staffs": public_campaign["staffs"],
        "school": public_campaign["school"],
        "camps": db_mapping_rows_to_dict(camps_unique),
        "campaign_info": db_mapping_rows_to_dict(campaign)[0],
    }

def get_sent_training(db, campaign_id:int):

    campaign = (
        db.query(
            Campaign.id.label("campaign_id"),
            Campaign.name.label("campaign_name"),
            Campaign.created_at.label("campaign_sent_date"),
            Training.name.label("training_event"),
            TrainingEvent.start.label("training_start"),
            EmailTemplate.title.label("template_title"),
            EmailTemplate.template.label("template_body"),
        )
        .select_from(Campaign)
        .join(TrainingEvent, TrainingEvent.id == Campaign.training_event_id)
        .join(Training, Training.id == TrainingEvent.training_id)
        .join(EmailTemplate, EmailTemplate.id == Campaign.template_id)
        .filter(Campaign.id == campaign_id)
        .all()
    )

    staffs = (
        db.query(
            (
                Staff.name + " " + Staff.lastname_father + " " + Staff.lastname_mother
            ).label("staff_fullname")
        )
        .select_from(StaffCampaign)
        .join(Staff, Staff.id == StaffCampaign.staff_id)
        .filter(StaffCampaign.campaign_id == campaign_id)
        .distinct()
        .all()
    )

    return {
        "staffs": staffs,
        "campaign_info": db_mapping_rows_to_dict(campaign)[0],
    }

def get_sent_candidates(db, campaign_id:int):

    campaign = (
        db.query(
            Campaign.id.label("campaign_id"),
            Campaign.name.label("campaign_name"),
            Campaign.created_at.label("campaign_sent_date"),
            Season.name.label("season_name"),
            EmailTemplate.title.label("template_title"),
            EmailTemplate.template.label("template_body"),
        )
        .select_from(Campaign)
        .join(Season, Season.id == Campaign.season_id)
        .join(EmailTemplate, EmailTemplate.id == Campaign.template_id)
        .filter(Campaign.id == campaign_id)
        .all()
    )

    staffs = (
        db.query(
            Staff.id, 
            (
                Staff.name + " " + Staff.lastname_father + " " + Staff.lastname_mother
            ).label("staff_fullname")
        )
        .select_from(StaffCampaign)
        .join(Staff, Staff.id == StaffCampaign.staff_id)
        .filter(StaffCampaign.campaign_id == campaign_id)
        .distinct()
        .all()
    )

    return {
        "staffs": staffs,
        "campaign_info": db_mapping_rows_to_dict(campaign)[0],
    }