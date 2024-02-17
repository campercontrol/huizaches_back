import csv
import pandas as pd
from io import StringIO
from sqlalchemy import text

from utils.timer import timer
import numpy as np

from model.catalogs.constant import Constant
from model.catalogs.currency import Currency
from model.catalogs.payment_account import PaymentAccount
from model.catalogs.staff_role import StaffRole
from model.catalogs.vaccine import Vaccine
from model.catalogs.food_restriction import FoodRestriction
from model.catalogs.licensed_medicine import LicensedMedicine
from model.catalogs.pathological_background import PathologicalBackground
from model.catalogs.pathological_background_family import PathologicalBackgroundFamily
from model.role import Role
from model.user import User
from model.campers.school import School
from model.campers.parent import Parent
from model.campers.camper_record import CamperRecord
from model.campers.camper import Camper
from model.campers.camper_food_restriction import CamperFoodRestriction
from model.campers.camper_licensed_medicine import CamperLicensedMedicine
from model.campers.camper_pathological_background_fm import CamperPathologicalBackgroundFamily
from model.campers.camper_pathological_background import CamperPathologicalBackground
from model.campers.camper_vaccine import CamperVaccine
from model.camps.location import Location 
from model.camps.season import Season
from model.camps.camp import Camp
from model.camps.camp_payments_accounts import CampPaymentAccount
from model.camps.camp_extra_charge import CampExtraCharge
from model.camps.camp_checkpoint import CampCheckpoint
from model.campers.camper_checkpoint import CamperCheckpoint
from model.camps.camp_extra_question import CampExtraQuestion
from model.campers.camper_extra_answer import CamperExtraAnswer
from model.campers.camper_comment import CamperComment
from model.camps.camper_in_camp import CamperInCamp
from model.trainings.training import Training
from model.trainings.training_event import TrainingEvent
from model.camps.camp_discount import CampDiscount
from model.staffs.staff_record import StaffRecord
from model.staffs.staff import Staff
from model.camps.staff_in_camp import StaffInCamp
from model.trainings.staff_in_training import StaffInTraining
from model.staffs.staff_food_restriction import StaffFoodRestriction
from model.staffs.staff_vaccine import StaffVaccine
from model.staffs.staff_comment import StaffComment
from model.trophies.trophy import Trophy
from model.trophies.trophy_season import TrophySeason
from model.trophies.trophy_staff import TrophyStaff
from model.mailings.email_template import EmailTemplate
from model.mailings.campaign import Campaign
from model.mailings.camper_campaign import CamperCampaign
from model.mailings.staff_campaign import StaffCampaign
from model.payments.payment_method import PaymentMethod
from model.payments.payment_transaction_type import PaymentTransactionType
from model.payments.payment import Payment
from model.payments.camper_extra_charge import CamperExtraCharge






from utils.db import SessionLocal

arr_error = []


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def read_and_format_catalogs_constant():
    print("catalogs_constant")
    pandas_filecontent = pd.read_json('csv/constants_2.json')

    listOfReading_Constant = [
        (Constant(
            uid = element["data"]["uid"],
            id = element["data"]["id"],
            value =element["data"]['value'], 
            num_id =element["data"]["num_id"], 
            language = element["data"]["language"],
            model_name = element["data"]["model_name"],
            created_at = element["data"]["created_at"],
            updated_at = element["data"]["updated_at"])
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Constant)

    return(listOfReading_Constant)


def search_in_costants(catalog,value):
    constant_filecontent = pd.read_json('csv/constants_2.json',convert_axes = True, encoding='utf-8')
    dataframe = constant_filecontent['data']
    arreglo = dataframe.to_numpy()
    arreglo2 = []

    value = value.replace('(','').replace(')','').replace('?','').replace('¿','').replace('+','\+').replace('*','')

    if catalog == 'gender':
        if value in ('male','m','man'):
            value = 'Male'
        elif value in ('female','f','woman'):
            value = 'Female'

    if catalog == 'can_swim':
        if value in ('','no','No','false'):
            value = 'no'
        elif value in ('si','Si','true'):
            value = 'si'
        elif value in ('yes','Yes'):
            value = 'yes'

    # print(f'Catalog {catalog}')
    # print(f'Value {value}')

    for i in arreglo:
        arreglo2.append(i)
    nei2 = pd.DataFrame(arreglo2)
    row_filter = nei2[nei2["model_name"].str.contains(catalog, case=False)]
    # print("*"*60 + " row_filter")
    # print(row_filter)
    # print("*"*60)
    result = row_filter[row_filter["value"].str.contains(value,case = False)]
    # print("*"*60 + " result")
    # print(result["value"])
    # print("*"*60)
    # if result.empty:
    #     print(f"NAN - {result} - {value}")
    # else:
    #     print(f"YES {result} - {value}")

    # print(result.size)

    # if result.size > 1:
    #     arr_error.append(value)

    return result.head(1)


def search_in_costants_grade(catalog,value):
    constant_filecontent = pd.read_json('csv/constants_2.json',convert_axes = True, encoding='utf-8')
    dataframe = constant_filecontent['data']
    arreglo = dataframe.to_numpy()
    arreglo2 = []

    #value = value.replace('(','').replace(')','').replace('?','').replace('¿','').replace('+','\+')

    for i in arreglo:
        arreglo2.append(i)
    nei2 = pd.DataFrame(arreglo2)
    row_filter = nei2[nei2["model_name"].str.contains(catalog, case=False)]
    result = row_filter[row_filter["num_id"] == value]

    # if result.empty:
    #     print(f"NAN - {result} - {value}")
    # else:
    #     print(f"YES {result} - {value}")
    # print(result)

    return result.head(1)




def read_and_format_catalogs_currency():
    print("catalogs_currency")
    with open("csv/catalogs_currency.csv","r") as catalogs_currency:
        content_catalogs_currency =  catalogs_currency.read()

    # print("Content")
    # print(content_catalogs_currency)

    pandas_filecontent = pd.read_csv(StringIO(content_catalogs_currency),sep="\"")

    # print("-"*30)
    # print(pandas_filecontent)

    listOfReading_Currency = [
        (Currency(
            id= element.id,
            name=element['name'], 
            symbol=element.symbol, 
            acronyms= element.acronyms,
            created_at= element.created if not 'NaN' else None,
            updated_at= element.updated if not 'NaN' else None)
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Currency)

    return listOfReading_Currency


def read_and_format_catalogs_payment_account():
    print("catalogs_payment_account")
    with open("csv/catalogs_payment_account.csv","r") as catalogs_payment_account:
        content_catalogs_payment_account =  catalogs_payment_account.read()

    # print("Content")
    # print(content_catalogs_currency)

    pandas_filecontent = pd.read_csv(StringIO(content_catalogs_payment_account),sep="\"")

    listOfReading_PaymentAccount = [
        (PaymentAccount(
            id= element.id,
            name= element['name'], 
            bank=element.bank, 
            account_number= element.account_number,
            clabe_number= element.clabe_number,
            created_at= element.created if not 'NaN' else None,
            updated_at= element.updated if not 'NaN' else None
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_PaymentAccount)

    return listOfReading_PaymentAccount


def read_and_format_catalogs_staffroles():
    print("catalogs_staffroles")
    with open("csv/catalogs_staff_role.csv","r") as catalogs_staffroles:
        content_catalogs_staffroles =  catalogs_staffroles.read()

    pandas_filecontent = pd.read_csv(StringIO(content_catalogs_staffroles),sep="\"")

    listOfReading_StaffRole = [
        (StaffRole(
            id= element.id,
            name= element['name'], 
            payment=element.payment, 
            color= element.color,
            created_at= element.created if not 'NaN' else None,
            updated_at= element.updated if not 'NaN' else None
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_StaffRole)

    return listOfReading_StaffRole


def read_and_format_catalogs_vaccines():
    print("catalogs_vaccines")
    with open("csv/catalogs_vaccine.csv","r") as catalogs_vaccines:
        content_catalogs_vaccines =  catalogs_vaccines.read()

    pandas_filecontent = pd.read_csv(StringIO(content_catalogs_vaccines),sep="\"")

    listOfReading_Vaccine = [
        (Vaccine(
            id = element.id,
            name = element['name'], 
            assigned_id = 1,#element.assigned, 
            order = element.order,
            created_at = element.created if not 'NaN' else None,
            updated_at = element.updated if not 'NaN' else None)
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return listOfReading_Vaccine


def read_and_format_catalogs_foodrestrictions():
    print("catalogs_foodrestrictions")
    with open("csv/catalogs_food_restriction.csv","r") as catalogs_food_restriction:
        content_catalogs_food_restriction =  catalogs_food_restriction.read()

    pandas_filecontent = pd.read_csv(StringIO(content_catalogs_food_restriction),sep="\"")

    listOfReading_FoodRestrinction = [
        (FoodRestriction(
            id = element.id,
            name = element['name'], 
            assigned_id = 1,#element.assigned, 
            order = element.order)
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return listOfReading_FoodRestrinction


def read_and_format_catalogs_licensed_medicine():
    print("catalogs_licensed_medicine")
    with open("csv/catalogs_licensed_medicine.csv","r") as catalogs_licensed_medicine:
        content_catalogs_licensed_medicine =  catalogs_licensed_medicine.read()

    pandas_filecontent = pd.read_csv(StringIO(content_catalogs_licensed_medicine),sep="\"")

    listOfReading_licensed_medicine  = [
        (LicensedMedicine(
            id = element.id,
            name = element['name'], 
            assigned_id = 1,#element.assigned, 
            order = element.order)
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return listOfReading_licensed_medicine


def read_and_format_catalogs_pathological_background():
    print("catalogs_pathological_background")
    with open("csv/catalogs_pathological_background.csv","r") as catalogs_pathological_background:
        content_catalogs_pathological_background =  catalogs_pathological_background.read()

    pandas_filecontent = pd.read_csv(StringIO(content_catalogs_pathological_background),sep="\"")

    listOfReading_pathological_background  = [
        (PathologicalBackground(
            id = element.id,
            name = element['name'], 
            assigned_id = 1,#element.assigned, 
            order = element.order,
            created_at = element.created if not 'NaN' else None,
            updated_at = element.updated if not 'NaN' else None
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return listOfReading_pathological_background


def read_and_format_catalogs_pathological_background_family():
    print("catalogs_pathological_background_family")
    with open("csv/catalogs_pathological_background_family.csv","r") as catalogs_pathological_background_family:
        content_catalogs_pathological_background_family =  catalogs_pathological_background_family.read()

    pandas_filecontent = pd.read_csv(StringIO(content_catalogs_pathological_background_family),sep="\"")

    content_catalogs_pathological_background_family  = [
        (PathologicalBackgroundFamily(
            id = element.id,
            name = element['name'], 
            assigned_id = 1,#element.assigned, 
            order = element.order,
            created_at = element.created if not 'NaN' else None,
            updated_at = element.updated if not 'NaN' else None
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_catalogs_pathological_background_family


def read_and_format_auth_group():
    print("auth_group")
    with open("csv/auth_group.csv","r") as auth_group:
        content_auth_group =  auth_group.read()

    pandas_filecontent = pd.read_csv(StringIO(content_auth_group),sep="\"")

    content_auth_group  = [
        (Role(
            id = element.id,
            name = element['name'], 
            is_active = True
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_auth_group


def read_and_format_auth_campercontrol_user():
    print("auth_campercontrol_user")
    with open("csv/auth_campercontrol_user.csv","r") as auth_campercontrol_user:
        content_auth_campercontrol_user =  auth_campercontrol_user.read()

    with open("csv/auth_campercontrol_user_groups.csv","r") as auth_campercontrol_user_groups:
        content_auth_campercontrol_user_groups =  auth_campercontrol_user_groups.read()

    with open("csv/limpio_staff_staff.csv","r") as staff_staff:
        content_staff_staff =  staff_staff.read()

    pandas_filecontent_staff = pd.read_csv(StringIO(content_staff_staff),sep="|",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent_staff.fillna(' ', inplace=True) 

    pandas_filecontent_group = pd.read_csv(StringIO(content_auth_campercontrol_user_groups),sep="\"")

    pandas_filecontent = pd.read_csv(StringIO(content_auth_campercontrol_user),sep="\"")

    content_auth_campercontrol_user_read = []

    for index, element in pandas_filecontent.iterrows():
        role = pandas_filecontent_group[pandas_filecontent_group["campercontroluser_id"] == element.id]["group_id"].values
        v_is_coordinator = False
        v_is_employee = False
        try:
            if role[0].item() == 2:
                #staff
                #print("Es staff")
                permisos = pandas_filecontent_staff[pandas_filecontent_staff["login_id"] == element.id]
                #print(permisos)
                if permisos.empty:
                    v_is_coordinator = False
                    v_is_employee = False
                else:
                    v_is_coordinator = True if permisos["coordinator"].values == 't' else False
                    v_is_employee = True if permisos["employee"].values == 't' else False
                #print(v_is_coordinator)
                #print(v_is_employee)
        except:
            v_is_coordinator = False
            v_is_employee = False

        content_auth_campercontrol_user_read.append(User(
            id = element.id,
            email = element["email"],
            hashed_pass = "GENERICA",### !!! poner contraseña generica 
            role_id = role[0].item() if len(role) > 0 else None,
            is_coordinator = v_is_coordinator,#verificar de donde vienen
            is_employee = v_is_employee,#verificar de donde vienen
            is_admin = True if element['is_superuser'] == 't' else False,
            is_superuser = True if element['is_superuser'] == 't' else False,
            is_active = True ,
            created_at = element.date_joined if not 'NaN' else None,
            updated_at = element.date_joined if not 'NaN' else None
            )
        )

    #print(listOfReading_Vaccine)

    return content_auth_campercontrol_user_read


def read_and_format_campers_school():
    print("campers_school")
    with open("csv/campers_school.csv","r") as campers_school:
        content_campers_school =  campers_school.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_campers_school),sep="\"")

    # print("-"*30)
    # print(pandas_filecontent)

    content_campers_school  = [
        (School(
            id = element.id,
            login_id = element.login_id if not 'NaN' else None,
            name = element['name'], 
            address = element.address,
            url = element.url,
            contact = element.contact,
            phone = element.phone,
            cellphone = element.cellphone,
            email = element.email,
            contact_second_name = element.contact_second_name,
            contact_second_phone = element.contact_second_phone,
            contact_second_cellphone = element.contact_second_cellphone,
            contact_second_email = element.contact_second_email,
            contact_third_name = element.contact_third_name,
            contact_third_phone = element.contact_third_phone,
            contact_third_cellphone = element.contact_third_cellphone,
            contact_third_email = element.contact_third_email,
            verify = True if element.verify == 't' else False,
            active = True if element.active == 't' else False,
            created_at = element.created if not 'NaN' else None,
            updated_at =element.updated if not 'NaN' else None
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_campers_school


def read_and_format_campers_parent():
    print("campers_parent")
    with open("csv/campers_parent.csv","r") as campers_parent:
        content_campers_parent =  campers_parent.read()

    pandas_filecontent = pd.read_csv(StringIO(content_campers_parent), on_bad_lines='warn',sep="\"",quoting=csv.QUOTE_MINIMAL,na_values=['N/A', 'NA', 'NULL',''])
    # print("-"*30)
    # print(pandas_filecontent)
    pandas_filecontent.fillna(' ', inplace=True) 


    content_campers_parent_read  = [
        (Parent(
            id = element.id,
            user_id= element.login_id ,
            tutor_name = element.tutor_name ,
            tutor_lastname_father = element.tutor_lastname_father ,
            tutor_lastname_mother = element.tutor_lastname_mother ,
            tutor_cellphone = element.tutor_cellphone ,
            tutor_home_phone = element.tutor_home_phone ,
            tutor_work_phone = element.tutor_work_phone ,
            contact_name = element.contact_name ,
            contact_lastname_father = element.contact_lastname_father ,
            contact_lastname_mother = element.contact_lastname_mother ,
            contact_cellphone = element.contact_cellphone,
            contact_home_phone = element.contact_home_phone ,
            contact_work_phone = element.contact_work_phone ,
            contact_email = element.contact_email ,
            created_at = element.created if not 'NaN' else None,
            updated_at =element.updated if not 'NaN' else None
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_campers_parent_read


def read_and_format_campers_camperrecords():
    print("campers_camperrecords")
    with open("csv/campers_camperrecords.csv","r") as campers_camperrecords:
        content_campers_camperrecords =  campers_camperrecords.read()

    pandas_filecontent = pd.read_csv(StringIO(content_campers_camperrecords), on_bad_lines='warn',sep="\"",quoting=csv.QUOTE_MINIMAL,na_values=['N/A', 'NA', 'NULL',''])
    # print("-"*30)
    # print(pandas_filecontent)
    #pandas_filecontent.fillna(' ', inplace=True) 


    content_campers_camperrecords_read  = [
        (CamperRecord(
            id = element.id.item(),
            attend = element.attend.item(),
            attended = element.attended.item(),
            total = element.total.item(),
            created_at = element.created if not 'NaN' else None,
            updated_at =element.updated if not 'NaN' else None
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_campers_camperrecords_read


def read_and_format_campers_camper():
    print("campers_camper")
    with open("csv/limpio_campers_camper.csv","r") as campers_camper:
        content_campers_camper =  campers_camper.read()

    pandas_filecontent = pd.read_csv(StringIO(content_campers_camper), on_bad_lines='warn',sep="|",na_values=['N/A', 'NA', 'NULL',''],low_memory=False)
    pandas_filecontent.fillna(' ', inplace=True) 

    content_campers_camper_read = []

    for index, element in pandas_filecontent.iterrows():
        # if index == 100:
        #     return content_campers_camper_read
        #print(f"element.id {element.id}")
        #==========================================================================
        #print(f"element['gender']{element['gender']}")
        gender_result = search_in_costants("gender",element['gender'])
        #print(f"gender_result {gender_result}") 
        if gender_result.empty:
            gender_result = 17
        else:
            gender_result = gender_result['id'].item()
        #==========================================================================
        #print(f"element['blood_type'] {element['blood_type']}")
        blood_type_result = search_in_costants("blood_type",element['blood_type'])
        #print(f"blood_type_result {blood_type_result}")
        if blood_type_result.empty:
            blood_type_result = 17
        else:
            blood_type_result = blood_type_result['id'].item()
        #==========================================================================
        #print(f"element['grade'] {element['grade']}")
        grade_result = search_in_costants_grade("grade",element['grade'])
        #print(f"grade_result {grade_result}")
        if grade_result.empty:
            grade_result = 17
        else:
            grade_result = grade_result['id'].item()
        #==========================================================================
        #print(f"element['grade'] {element['grade']}")
        can_swim_result = search_in_costants("can_swim",element['can_swim'])
        #print(f"grade_result {grade_result}")
        if can_swim_result.empty:
            can_swim_result = 17
        else:
            can_swim_result = can_swim_result['id'].item()


        content_campers_camper_read.append(Camper(
            id = element.id,
            name = element['name'],
            lastname_father = element['lastname_father'],
            photo = element['photo'],
            lastname_mother = element['lastname_mother'],
            gender_id = gender_result,
            blood_type = blood_type_result,#
            grade = grade_result,#
            can_swim = can_swim_result,#
            birthday = element["birthday"],
            height = element["height"] if element["height"] != ' ' else 0,
            weight = element["weight"] if element["weight"] != ' ' else 0,
            school_id = None if (element["school_id"] == ' ' or element["school_id"] == 0 or element["school_id"] == '0')  else element["school_id"],
            school_other = element["school_other"],
            email = element["email"],
            affliction = element["affliction"],
            temporal_blood_type = element["blood_type"],
            heart_problems = element["heart_problems"],
            psicology_treatments = element["psicology_treatments"],
            prevent_activities = element["prevent_activities"],
            drug_allergies = element["drug_allergies"],
            other_allergies = element["other_allergies"],
            nocturnal_disorders = element["nocturnal_disorders"],
            phobias = element["phobias"],
            drugs = element["drugs"],
            doctor_precall = True if element["doctor_precall"] == 't' else False,
            prohibited_foods = element["prohibited_foods"],
            comments_admin = element["comments_admin"],
            insurance = True if element["insurance"] == 't' else False,
            insurance_company = element["insurance_company"],
            insurance_number = element["insurance_number"],
            security_social_number = element["security_social_number"],
            contact_name = element["contact_name"],
            contact_relation = element["contact_relation"],
            contact_homephone = element["contact_homephone"],
            contact_cellphone = element["contact_cellphone"],
            parent_id = None if element["parent_id"] == ' ' else element["parent_id"],
            record_id = None if element["record_id"] == ' ' else element["record_id"],
            created_at = element.created if not 'NaN' else None,
            updated_at =element.updated if not 'NaN' else None
            )    
        )

    # print(content_campers_camper_read)

    return content_campers_camper_read


def read_and_format_campers_camper_food_restriction():
    print("campers_camper_food_restriction")
    with open("csv/campers_camper_food_restriction.csv","r") as campers_camper_food_restriction:
        content_campers_camper_food_restriction =  campers_camper_food_restriction.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_campers_camper_food_restriction),sep="\"")

    # print("-"*30)
    # print(pandas_filecontent)

    content_campers_camper_food_restriction  = [
        (CamperFoodRestriction(
            id = element.id.item(),
            camper_id = element["camper_id"].item(),
            food_restriction_id = element["foodrestrictions_id"].item(),
            is_active = True
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_campers_camper_food_restriction


def read_and_format_campers_camper_authorized_drugs():
    print("campers_camper_licensed_medicine")
    with open("csv/campers_camper_licensed_medicine.csv","r") as campers_camper_authorized_drugs:
        content_campers_camper_authorized_drugs =  campers_camper_authorized_drugs.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_campers_camper_authorized_drugs),sep="\"")

    # print("-"*30)
    # print(pandas_filecontent)

    content_campers_camper_authorized_drugs  = [
        (CamperLicensedMedicine(
            id = element.id.item(),
            camper_id = element["camper_id"].item(),
            licensed_medicine_id = element["licensedmedicine_id"].item(),
            is_active = True
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_campers_camper_authorized_drugs


def read_and_format_campers_camper_pathological_background_family():
    print("campers_camper_pathological_background_family")
    with open("csv/campers_camper_pathological_background_family.csv","r") as campers_camper_pathological_background_family:
        content_campers_camper_pathological_background_family =  campers_camper_pathological_background_family.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_campers_camper_pathological_background_family),sep="\"")

    # print("-"*30)
    # print(pandas_filecontent)

    content_campers_camper_pathological_background_family  = [
        (CamperPathologicalBackgroundFamily(
            id = element.id.item(),
            camper_id = element["camper_id"].item(),
            pathological_background_family_id = element["pathological_background_family_id"].item(),
            is_active = True
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_campers_camper_pathological_background_family


def read_and_format_campers_camper_pathological_background():
    print("campers_camper_pathological_background")
    with open("csv/campers_camper_pathological_background.csv","r") as campers_camper_pathological_background:
        content_campers_camper_pathological_background =  campers_camper_pathological_background.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_campers_camper_pathological_background),sep="\"")

    # print("-"*30)
    # print(pandas_filecontent)

    content_campers_camper_pathological_background  = [
        (CamperPathologicalBackground(
            id = element.id.item(),
            camper_id = element["camper_id"].item(),
            pathological_background_id = element["pathological_background_id"].item(),
            is_active = True
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_campers_camper_pathological_background


def read_and_format_campers_camper_vaccines():
    print("campers_camper_vaccines")
    with open("csv/campers_camper_vaccines.csv","r") as campers_camper_vaccines:
        content_campers_camper_vaccines =  campers_camper_vaccines.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_campers_camper_vaccines),sep="\"")

    # print("-"*30)
    # print(pandas_filecontent)

    content_campers_camper_vaccines  = [
        (CamperVaccine(
            id = element.id.item(),
            camper_id = element["camper_id"].item(),
            vaccine_id = element["vaccines_id"].item(),
            is_active = True
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_campers_camper_vaccines


def read_and_format_camps_location():
    print("camps_location")
    with open("csv/limpio_camps_location.csv","r") as camps_location:
        content_camps_location =  camps_location.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_location),sep="|",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # print(pandas_filecontent)

    content_camps_location  = [
        (Location(
            id = element.id,
            name = element["name"],
            phone = element["phone"],
            email = element["email"],
            contact = element["contact"],
            address = element["address"],
            url = element["url"],
            active = True if element["active"] == 't' else False,
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_location


def read_and_format_camps_season():
    print("camps_season")
    with open("csv/camps_season.csv","r") as camps_season:
        content_camps_season =  camps_season.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_season),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # print(pandas_filecontent)

    content_camps_season  = [
        (Season(
            id = element.id,
            name = element["name"],
            current = True if element["current"] == 't' else False,
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_season


def read_and_format_camps_camp():
    print("camps_camp")
    with open("csv/limpio_camps_camp.csv","r") as camps_camp:
        content_camps_camp =  camps_camp.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_camp),sep="|",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
    # for index, element in pandas_filecontent.iterrows():
    #     print(element)
        

    content_camps_camp  = [
        (Camp(
            id = element.id,
            name = element["name"],
            start = element["start"],
            end = element["end"],
            start_registration = element["start_registration"],
            end_registration = element["end_registration"],
            registration = True if element["registration"] == 't' else False,
            url = element["url"],
            special_message = element["special_message"],
            special_message_admin = element["special_message_admin"],
            public_price = element["public_price"] if element["public_price"] != ' ' else 0.0,
            show_payment_parent = True if element["show_payment_parent"] == 't' else False ,
            show_rebate_parent = True if element["show_rebate_parent"] == 't' else False ,
            show_paypal_button = True if element["show_paypal_button"] == 't' else False ,
            show_payment_order = True if element["show_payment_order"] == 't' else False ,
            reminder_camp_days = element["reminder_camp_days"] if element["reminder_camp_days"] != ' ' else 0,
            reminder_discount_days = element["reminder_discount_days"] if element["reminder_discount_days"] != ' ' else 0,
            insurance = element["insurance"] if element["insurance"] != ' ' else 0.0,
            venue = element["venue"],
            photo_url = element["photo_url"],
            photo_password = element["photo_password"],
            medical_report = element["medical_report"],
            occupancy_camp = element["occupancy_camp"] if element["occupancy_camp"] != ' ' else 0 ,
            active = True if element["active"] == 't' else False,
            general_camp = True,#element["general_camp"],
            currency_id = element["currency_id"] if element["currency_id"] != ' ' else None,
            location_id = element["location_id"] if element["location_id"] != ' ' else None,
            school_id = element["school_id"] if element["school_id"] != ' ' else None,
            season_id = element["season_id"] if element["season_id"] != ' ' else None,
            # current = True if element["current"] == 't' else False,
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_camp


def read_and_format_camps_camp_payments_accounts():
    print("camps_camp_payments_accounts")
    with open("csv/camps_camp_payments_accounts.csv","r") as camps_camp_payments_accounts:
        content_camps_camp_payments_accounts =  camps_camp_payments_accounts.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_camp_payments_accounts),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_camps_camp_payments_accounts  = [
        (CampPaymentAccount(
            id = element.id.item(),
            camp_id = element["camp_id"].item(),
            paymentaccount_id = element["paymentaccounts_id"].item()
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_camp_payments_accounts


def read_and_format_camps_campextracharge():
    print("camps_campextracharge")
    with open("csv/camps_campextracharge.csv","r") as camps_campextracharge:
        content_camps_campextracharge =  camps_campextracharge.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_campextracharge),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_camps_campextracharge  = [
        (CampExtraCharge(
            id = element.id,
            name = element["name"],
            price = element["price"],
            currency_id = element["currency_id"],
            camp_id = element["camp_id"],
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_campextracharge


def read_and_format_camps_checkpoint():
    print("camps_checkpoint")
    with open("csv/camps_checkpoint.csv","r") as camps_checkpoint:
        content_camps_checkpoint =  camps_checkpoint.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_checkpoint),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_camps_checkpoint  = [
        (CampCheckpoint(
            id = element.id,
            name = element["name"],
            chekpoint_date = element["date"],
            order = element["order"],
            camp_id = element["camp_id"],
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_checkpoint


def read_and_format_camps_checkpointcamper():
    print("camps_checkpointcamper")
    with open("csv/camps_checkpointcamper.csv","r") as camps_checkpointcamper:
        content_camps_checkpointcamper =  camps_checkpointcamper.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_checkpointcamper),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_camps_checkpointcamper  = [
        (CamperCheckpoint(
            id = element.id,
            checkin =  True if element["checkin"] == 't' else False,
            checkin_date = element["checkin_date"],
            camper_id = element["camper_id"],
            checkpoint_id = element["checkpoint_id"],
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_checkpointcamper


def read_and_format_camps_extraquestion():
    print("camps_extraquestion")
    with open("csv/camps_extraquestion.csv","r") as camps_extraquestion:
        content_camps_extraquestion =  camps_extraquestion.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_extraquestion),sep="|",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_camps_extraquestion = [
        (CampExtraQuestion(
            id = element.id,
            question = element["question"],
            is_required = True if element["is_required"] == 't' else False,
            camp_id = element["camp_id"],
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_extraquestion


def read_and_format_campers_extraanswers():
    print("campers_extraanswers")
    with open("csv/campers_extraanswers.csv","r") as campers_extraanswers:
        content_campers_extraanswers =  campers_extraanswers.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_campers_extraanswers),sep="|",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_campers_extraanswers  = [
        (CamperExtraAnswer(
            id = element.id,
            answer = element["answer"],
            camper_id = element["camper_id"],
            question_id = element["question_id"],
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_campers_extraanswers


def read_and_format_campers_campercomment():
    print("campers_campercomment")
    with open("csv/limpio_campers_campercomment.csv","r") as campers_campercomment:
        content_campers_campercomment =  campers_campercomment.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_campers_campercomment),sep="|",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_campers_campercomment  = [
        (CamperComment(
            id = element.id,
            comment = element["comment"],
            is_public = True if element["is_public"] == 't' else False,
            show_to = element["show_to"] if element["show_to"] != ' ' else None ,
            camp_id = element["camp_id"] if element["camp_id"] != ' ' else None ,
            camper_id = element["camper_id"] if element["camper_id"] != ' ' else None ,
            user_id = element["user_id"] if element["user_id"] != ' ' else None ,
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_campers_campercomment


def read_and_format_camps_camperincamp():
    print("camps_camperincamp")
    with open("csv/camps_camperincamp.csv","r") as camps_camperincamp:
        content_camps_camperincamp =  camps_camperincamp.read()

    pandas_filecontent = pd.read_csv(StringIO(content_camps_camperincamp),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    status_dict = {
        0 : 34,
        1 : 35,
        2 : 36, 
        3 : 37
    }

    # print("-"*30)
    # # print(pandas_filecontent)

    content_camps_camperincamp  = [
        (CamperInCamp(
            id = element.id,
            status = status_dict.get(element["status"],17),
            payment_balance = element["payment_balance"],
            camp_id = element["camp_id"] if element["camp_id"] != ' ' else None ,
            camper_id = element["camper_id"] if element["camper_id"] != ' ' else None ,
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_camperincamp


def read_and_format_camps_training():
    print("camps_training")
    with open("csv/camps_training.csv","r") as camps_training:
        content_camps_training =  camps_training.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_training),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_camps_training  = [
        (Training(
            id = element.id,
            name = element["name"],
            photo = element["photo"],
            description = element["description"],
            url = element["url"],
            active = True if element["active"] == 't' else False,
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_training


def read_and_format_camps_trainingevent():
    print("camps_trainingevent")
    with open("csv/camps_trainingevent.csv","r") as camps_trainingevent:
        content_camps_trainingevent =  camps_trainingevent.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_trainingevent),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_camps_trainingevent  = [
        (TrainingEvent(
            id = element.id,
            start = element["start"],
            end = element["end"],
            location = element["location"],
            open_enrollment = True if element["open_enrollment"] == 't' else False,
            active = True if element["active"] == 't' else False,
            season_id = element["season_id"],
            training_id = element["training_id"],
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_trainingevent


def read_and_format_camps_campdiscount():
    print("camps_campdiscount")
    with open("csv/camps_campdiscount.csv","r") as camps_campdiscount:
        content_camps_campdiscount =  camps_campdiscount.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_campdiscount),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_camps_campdiscount  = [
        (CampDiscount(
            id = element.id,
            name = element["name"],
            amount = element["amount"],
            date_start = element["date_start"],
            date_end = element["date_end"],
            camp_id = element["camp_id"] if element["camp_id"] != ' ' else None ,
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_campdiscount


def read_and_format_staff_userrecords():
    print("staff_userrecords")
    with open("csv/staff_userrecords.csv","r") as staff_userrecords:
        content_staff_userrecords =  staff_userrecords.read()

    pandas_filecontent = pd.read_csv(StringIO(content_staff_userrecords), on_bad_lines='warn',sep="\"",quoting=csv.QUOTE_MINIMAL,na_values=['N/A', 'NA', 'NULL',''])
    # print("-"*30)
    # print(pandas_filecontent)
    #pandas_filecontent.fillna(' ', inplace=True) 


    content_staff_userrecords  = [
        (StaffRecord(
            id = element.id.item(),
            attend = element.attend.item(),
            attended = element.attended.item(),
            total = element.total.item(),
            created_at = element.created if not 'NaN' else None,
            updated_at =element.updated if not 'NaN' else None
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_staff_userrecords


def read_and_format_staff_staff():
    print("staff_staff")
    with open("csv/limpio_staff_staff.csv","r") as staff_staff:
        content_staff_staff =  staff_staff.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_staff_staff),sep="|",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)

    content_staff_staff = []

    for index, element in pandas_filecontent.iterrows():
        content_staff_staff.append(
            Staff(
            id = element.id,
            name =element["name"],
            lastname_father = element["lastname_father"],
            lastname_mother = element["lastname_mother"],
            gender_id = 17,
            photo = element["photo"],
            curp = element["curp"],
            rfc = element["rfc"],
            cellphone = element["cellphone"],
            home_phone = element["home_phone"],
            birthday = element["birthday"],
            affliction = element["affliction"],
            blood_type = element["blood_type"],
            drug_allergies = element["drug_allergies"],
            other_allergies = element["other_allergies"],
            nocturnal_disorders = element["nocturnal_disorders"],
            phobias = element["phobias"],
            drugs = element["drugs"],
            prohibited_foods = element["prohibited_foods"],
            bio = element["bio"],
            comments = element["comments"],
            employee = True if element["employee"] == 't' else False,
            coordinator = True if element["coordinator"] == 't' else False,
            cv = element["cv"],
            facebook = element["facebook"],
            staff_contact_name = element["staff_contact_name"],
            staff_contact_relation = element["staff_contact_relation"],
            staff_contact_homephone = element["staff_contact_homephone"],
            staff_contact_cellphone = element["staff_contact_cellphone"],
            employee_email_send = True if element["employee_email_send"] == 't' else False,
            login_id = element["login_id"] if element["login_id"] != ' ' else None,
            record_id = element["record_id"] if element["record_id"] != ' ' else None,
            season_id = element["season_id"] if element["season_id"] != ' ' else None,
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )

    #print(listOfReading_Vaccine)

    return content_staff_staff


def read_and_format_camps_staffincamp():
    print("camps_staffincamp")
    with open("csv/limpio_camps_staffincamp.csv","r") as camps_staffincamp:
        content_camps_staffincamp =  camps_staffincamp.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_staffincamp),sep="|",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_camps_staffincamp  = [
        (StaffInCamp(
            id = element.id,
            confirmed_staff = True if element["confirmed_staff"] == 't' else False,
            assigned_role_id = element["assigned_role_id"] if element["assigned_role_id"] != ' ' else None,
            camp_id = element["camp_id"] if element["camp_id"] != ' ' else None,
            staff_id = element["staff_id"] if element["staff_id"] != ' ' else None,
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_staffincamp


def read_and_format_camps_staffintraining():
    print("camps_staffintraining")
    with open("csv/camps_staffintraining.csv","r") as camps_staffintraining:
        content_camps_staffintraining =  camps_staffintraining.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_camps_staffintraining),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_camps_staffintraining  = [
        (StaffInTraining(
            id = element.id,
            assist = True if element["assist"] == 't' else False,
            confirmed_staff = True if element["confirmed_staff"] == 't' else False,
            staff_id = element["staff_id"] if element["staff_id"] != ' ' else None,
            training_event_id = element["training_event_id"] if element["training_event_id"] != ' ' else None,
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_camps_staffintraining


def read_and_format_staff_staff_food_restriction():
    print("staff_staff_food_restriction")
    with open("csv/staff_staff_food_restriction.csv","r") as staff_staff_food_restriction:
        content_staff_staff_food_restriction =  staff_staff_food_restriction.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_staff_staff_food_restriction),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_staff_staff_food_restriction = [
        (StaffFoodRestriction(
            id = element.id.item(),
            staff_id = element["staff_id"].item() ,
            food_restriction_id = element["foodrestrictions_id"].item() ,
            is_active = True
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_staff_staff_food_restriction


def read_and_format_staff_staff_vaccines():
    print("staff_staff_vaccines")
    with open("csv/staff_staff_vaccines.csv","r") as staff_staff_vaccines:
        content_staff_staff_vaccines =  staff_staff_vaccines.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_staff_staff_vaccines),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_staff_staff_vaccines = [
        (StaffVaccine(
            id = element.id.item(),
            staff_id = element["staff_id"].item() ,
            vaccine_id = element["vaccines_id"].item() ,
            is_active = True
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_staff_staff_vaccines


def read_and_format_staff_staffcomment():
    print("staff_staffcomment")
    with open("csv/staff_staffcomment.csv","r") as staff_staffcomment:
        content_staff_staffcomment =  staff_staffcomment.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_staff_staffcomment),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
        

    content_staff_staffcomment = [
        (StaffComment(
            id = element.id,
            comment = element["comment"],
            is_public = True if element["is_public"] == 't' else False ,
            show_to = 17,#element["show_to"],
            staff_id = element["staff_id"],
            user_id = element["user_id"],
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_staff_staffcomment


def read_and_format_trophy_trophy():
    print("trophy_trophy")
    with open("csv/trophy_trophy.csv","r") as trophy_trophy:
        content_trophy_trophy =  trophy_trophy.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_trophy_trophy),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)

    content_trophy_trophy = [
        (Trophy(
            id = element.id,
            name = element["name"],
            description = element["description"],
            photo = element["photo"],
            active = True if element["active"] == 't' else False,
            trophy_type = 84 if element["trophy_type"] == 1 else 85
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_trophy_trophy


def read_and_format_trophy_trophystaff():
    print("trophy_trophystaff")
    with open("csv/trophy_trophystaff.csv","r") as trophy_trophystaff:
        content_trophy_trophystaff =  trophy_trophystaff.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_trophy_trophystaff),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)

    content_trophy_trophystaff = [
        (TrophySeason(
            id = element.id.item(),
            trophy_id = element["trophy_id"].item(),
            season_id = element["season_id"].item()
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_trophy_trophystaff


def read_and_format_trophy_trophystaff_holder():
    print("trophy_trophystaff_holder")
    with open("csv/trophy_trophystaff_holder.csv","r") as trophy_trophystaff_holder:
        content_trophy_trophystaff_holder =  trophy_trophystaff_holder.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_trophy_trophystaff_holder),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)

    content_trophy_trophystaff_holder = [
        (TrophyStaff(
            id = element.id.item(),
            trophy_season_id = element["trophystaff_id"].item(),
            staff_id = element["staff_id"].item()
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_trophy_trophystaff_holder


def read_and_format_mailing_emailtemplate():
    print("mailing_emailtemplate")
    with open("csv/mailing_emailtemplate.csv","r") as mailing_emailtemplate:
        content_mailing_emailtemplate =  mailing_emailtemplate.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_mailing_emailtemplate),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)

    content_mailing_emailtemplate = [
        (EmailTemplate(
            id = element.id,
            template_type = 17,
            title = element["title"],
            template = element["template"],
            order = element["order"],
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_mailing_emailtemplate


def read_and_format_mailing_campaign():
    print("mailing_campaign")
    with open("csv/limpio_mailing_campaign.csv","r") as mailing_campaign:
        content_mailing_campaign =  mailing_campaign.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_mailing_campaign),sep="|",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)

    content_mailing_campaign = [
        (Campaign(
            id = element.id,
            name = element["name"],
            camp_parents = True if element["camp_parents"] == 't' else False,
            camp_staff = True if element["camp_staff"] == 't' else False,
            camp_school = True if element["camp_school"] == 't' else False,
            active_time = element["active_time"],
            send = True if element["send"] == 't' else False,
            camp_id = None if element["camp_id"] == ' ' else element["camp_id"],
            season_id = None if element["season_id"]  == ' ' else element["season_id"],
            send_type_id = 17,#element["send_type_id"],
            training_event_id = None,#element["training_event_id"],
            template_id = element["template_id"],
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_mailing_campaign


def read_and_format_mailing_campaign_campers():
    print("mailing_campaign_campers")
    with open("csv/mailing_campaign_campers.csv","r") as mailing_campaign_campers:
        content_mailing_campaign_campers =  mailing_campaign_campers.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_mailing_campaign_campers),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)

    content_mailing_campaign_campers = [
        (CamperCampaign(
            id = element.id.item(),
            camp_id = None,
            campaign_id = element["campaign_id"].item(),
            camper_id = element["camper_id"].item(),
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_mailing_campaign_campers


def read_and_format_mailing_campaign_staff():
    print("mailing_campaign_staff")
    with open("csv/mailing_campaign_staff.csv","r") as mailing_campaign_staff:
        content_mailing_campaign_staff =  mailing_campaign_staff.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_mailing_campaign_staff),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
    if pandas_filecontent.empty:
        return []

    content_mailing_campaign_staff = [
        (StaffCampaign(
            id = element.id.item(),
            campaign_id = element["campaign_id"].item(),
            camp_id = None,
            staff_id = element["staff_id"].item(),
            training_event_id = None,
            season_id = None,
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_mailing_campaign_staff


def read_and_format_payments_paymentmethod():
    print("payments_paymentmethod")
    with open("csv/payments_paymentmethod.csv","r") as payments_paymentmethod:
        content_payments_paymentmethod =  payments_paymentmethod.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_payments_paymentmethod),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
    if pandas_filecontent.empty:
        return []

    content_payments_paymentmethod = [
        (PaymentMethod(
            id = element.id,
            name = element["name"],
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_payments_paymentmethod


def read_and_format_payments_paymenttransactiontype():
    print("payments_paymenttransactiontype")
    with open("csv/payments_paymenttransactiontype.csv","r") as payments_paymenttransactiontype:
        content_payments_paymenttransactiontype =  payments_paymenttransactiontype.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_payments_paymenttransactiontype),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
    if pandas_filecontent.empty:
        return []

    content_payments_paymenttransactiontype = [
        (PaymentTransactionType(
            id = element.id,
            name = element["name"],
            movement = element["movement"],
            created_at = element["created"],
            updated_at = element["updated"]
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_payments_paymenttransactiontype


def read_and_format_payments_payment():
    print("payments_payment")
    with open("csv/limpio_payments_payment.csv","r") as payments_payment:
        content_payments_payment =  payments_payment.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_payments_payment),sep="|",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
    if pandas_filecontent.empty:
        return []

    content_payments_payment = [
        (Payment(
            id = element.id,
            paid = True if element["paid"] == 't' else False,
            payment_date = element["payment_date"] if element["payment_date"] != ' ' else None,
            payment_amount = element["payment_amount"],
            txn_number = element["txn_number"],
            camp_id = element["camp_id"] if element["camp_id"] != ' ' else None  ,
            camper_id = element["camper_id"] if element["camper_id"] != ' ' else None ,
            currency_id = element["currency_id"] if element["currency_id"] != ' ' else None ,
            parent_id = element["parent_id"] if element["parent_id"] != ' ' else None ,
            payment_method_id = element["payment_method_id"] if element["payment_method_id"] != ' ' else None  ,
            txn_type_id = element["txn_type_id"] if element["txn_type_id"] != ' ' else None  ,
            created_at = element["created"] if element["created"] != ' ' else None,
            updated_at = element["updated"] if element["updated"] != ' ' else None
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_payments_payment


def read_and_format_payments_camperextracharge():
    print("payments_camperextracharge")
    with open("csv/payments_camperextracharge.csv","r") as payments_camperextracharge:
        content_payments_camperextracharge =  payments_camperextracharge.read()

    #pandas_filecontent = pd.read_csv(StringIO(content_campers_school), on_bad_lines='warn') #Validar renglones con errores
    pandas_filecontent = pd.read_csv(StringIO(content_payments_camperextracharge),sep="\"",low_memory=False, on_bad_lines='warn',na_values=['N/A', 'NA', 'NULL',''])
    pandas_filecontent.fillna(' ', inplace=True) 

    # print("-"*30)
    # # print(pandas_filecontent)
    if pandas_filecontent.empty:
        return []

    content_payments_camperextracharge = [
        (CamperExtraCharge(
            id = element.id,
            is_selected = True if element["is_selected"] == 't' else False,
            camper_id = element["camper_id"] if element["camper_id"] != ' ' else None ,
            extra_charge_id = element["extra_charge_id"] if element["extra_charge_id"] != ' ' else None ,
            created_at = element["created"] if element["created"] != ' ' else None,
            updated_at = element["updated"] if element["updated"] != ' ' else None
            )
        )for index, element in pandas_filecontent.iterrows()
    ]

    #print(listOfReading_Vaccine)

    return content_payments_camperextracharge





def save_table(db,reg_table):
    try:
        result = db.add_all(reg_table)
        db.commit()
    except Exception as ex:
        result = 0
        print(f"No se pudo guardar en la base de datos: {ex}")
    return result


def save_table_individual(db,reg_table):
    try:
        result = db.add(reg_table)
        db.commit()
    except Exception as ex:
        result = 0
        print(f"No se pudo guardar en la base de datos: {ex}")
    return result


def truncate_table(db,tablename):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from dotenv import find_dotenv, load_dotenv
    import os

    load_dotenv(find_dotenv())
    user = os.getenv("DB_USER", "")
    password = os.getenv("DB_PASS", "")
    host = os.getenv("DB_HOST", "")
    port = os.getenv("DB_PORT", "")
    db = os.getenv("DB_NAME", "")

    # print(f"user {user}")
    # print(f"password {password}")
    # print(f"host {host}")
    # print(f"port {port}")
    # print(f"db {db}")

    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

    # Crea una conexión a la base de datos utilizando SQLAlchemy
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    connection = engine.raw_connection()
    cursor = connection.cursor()
    
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # Consulta SQL para truncar la tabla saltando las restricciones
    

    #txt = f"TRUNCATE TABLE {tablename} CASCADE;"
    txt = f"DELETE FROM {tablename};"
    sql_truncate = text(txt)

    # resultado = cursor.execute(txt)
    
    #==================

    # resultado = session.execute(sql_truncate)

    # print(resultado)
    
    #==================

    # Ejecuta la consulta SQL
    with engine.connect() as conexion:
        resultado = conexion.execute(sql_truncate)
        print(resultado.mappings().all())

    return resultado
    ###=======================================
    # try:
    #     txt = f"TRUNCATE TABLE {tablename} RESTART IDENTITY CASCADE"
    #     print(txt)
    #     sql_truncate = text(txt)
    #     print(sql_truncate)
    #     result = db.execute(sql_truncate)
    #     #result = db.query(tablename).delete().execute()
    #     #result = db.rollback()
    # except Exception as ex:
    #     result = 0
    #     print(f"Error en proceso de truncar tablas {ex}")
    # return result


def truncate_database(db,count_tables_inserted,arr_tables_inserted):
    for i in arr_tables_inserted:
        print(1)
        truncate_table(db,i)

    return {"mensaje":"Tablas truncada por error de insersion","process":arr_tables_inserted}


@timer
def migrar_base_v2_to_v3(db):
    """
        [X]catalogs_currencies -> catalogs_currency
        [X]catalogs_paymentaccounts -> catalogs_payment_account
        [X]catalogs_staffroles -> catalogs_staff_role
        [X]catalogs_vaccines -> catalogs_vaccine 
        [X]catalogs_foodrestrictions -> catalogs_food_restriction
        [X]catalogs_licensedmedicine - > catalogs_licensed_medicine
        [X]catalogs_pathological_background -> catalogs_pathological_background 
        [X]catalogs_pathological_background_family -> catalogs_pathological_background_family
        [X]auth_group -> Role  
        [X]auth_campercontrol_user_groups
        [X]auth_campercontrol_user -> User
        [X]campers_school -> campers_school
        [X]campers_parent -> campers_parent
        [X]campers_camperrecords -> campers_camperrecords
        [X]campers_camper -> campers_camper
        [X]campers_camper_food_restriction -> campers_camper_food_restriction
        [X]campers_camper_authorized_drugs -> campers_camper_licensed_medicine
        [X]campers_camper_pathological_background_family
        [X]campers_camper_pathological_background
        [X]campers_camper_vaccines -> campers_camper_vaccines
        [X]camps_location -> camps_location
        [X]camps_season -> camps_season
        [X]camps_camp -> camps_camp
        [X]camps_camp_payments_accounts -> camps_camp_payments_accounts
        [X]camps_campextracharge -> camps_campextracharge
        [X]camps_checkpoint -> camps_checkpoint
        [X]camps_checkpointcamper
        [X]camps_extraquestion -> camps_extraquestion
        [X]campers_extraanswers -> campers_extraanswers
        [X]campers_campercomment -> campers_campercomment
        [-]camps_camp_campers ->
        [X]camps_camperincamp
        [-]camps_campfile
        [-]campers_extrafile
        [X]camps_training
        [X]camps_trainingevent
        [X]camps_campdiscount
        [X]staff_userrecords
        [X]staff_staff
        [-]camps_camp_staff
        [X]camps_staffincamp
        [-]camps_staffsendercamp
        [-]camps_tribe
        [-]camps_tribecamp
        [-]camps_tribecamper
        [X]camps_staffintraining
        [-]staff_skill
        [-]staff_staff_skills #-------

        [X]staff_staff_food_restriction
        [X]staff_staff_vaccines
        [X]staff_staffcomment

        [-]camps_camp_staff_available

        [X]trophy_trophy
        [X]trophy_trophystaff
        [X]trophy_trophystaff_holder

        [X]mailing_emailtemplate
        [X]mailing_campaign
        [X]mailing_campaign_campers
        [-]mailing_campaign_camps
        [-]mailing_campaign_parents
        [-]mailing_campaign_training
        [X]mailing_campaign_staff

        [X]payments_paymentmethod
        [X]payments_paymenttransactiontype
        [X]payments_payment
        [X]payments_camperextracharge



        -auth_permission
        -auth_campercontrol_user_user_permissions
        -auth_group_permissions
        -menu_menu    
        -medical_doctor
        -medical_staffmedicalvisit
        -medical_campermedicalvisit
        -grouping_groupingtype
        -grouping_grouping
        -grouping_groupingcamp
        -grouping_groupingcamper
        -store_storetransactiontype
        -store_storepayment
        -teacher_teacher
        -teacher_teacher_vaccines
        -teacher_teacher_food_restriction
        -scheduler_cronjob
        -scheduler_repeatablejob
        -scheduler_scheduledjob

    """
        
    count_tables_inserted = 0
    arr_tables_inserted = []

    #------------------------------------------------

    listOfReading_Constant = read_and_format_catalogs_constant()
    print("-"*30)
    #print(listOfReading_Constant)
    if (save_table(db,listOfReading_Constant) == 0):
        arr_tables_inserted.append(Constant)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Constant)
    count_tables_inserted += 1

    # #------------------------------------------------

    listOfReading_Currency = read_and_format_catalogs_currency()
    print("-"*30)
    #print(listOfReading_Currency)
    if (save_table(db,listOfReading_Currency) == 0):
        arr_tables_inserted.append(Currency)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Currency)
    count_tables_inserted += 1


    # #------------------------------------------------

    listOfReading_PaymentAccount = read_and_format_catalogs_payment_account()
    print("-"*30)
    #print(listOfReading_PaymentAccount)
    if (save_table(db,listOfReading_PaymentAccount) == 0):
        arr_tables_inserted.append(PaymentAccount)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(PaymentAccount)
    count_tables_inserted += 1

    # #------------------------------------------------

    listOfReading_StaffRole = read_and_format_catalogs_staffroles()
    print("-"*30)
    #print(listOfReading_StaffRole)
    if (save_table(db,listOfReading_StaffRole) == 0):
        arr_tables_inserted.append(StaffRole)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(StaffRole)
    count_tables_inserted += 1

    # #------------------------------------------------

    listOfReading_Vaccines = read_and_format_catalogs_vaccines()
    print("-"*30)
    #print(listOfReading_Vaccines)
    if (save_table(db,listOfReading_Vaccines) == 0):
        arr_tables_inserted.append(Vaccine)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Vaccine)
    count_tables_inserted += 1

    # #------------------------------------------------

    listOfReading_FoodRestriction = read_and_format_catalogs_foodrestrictions()
    print("-"*30)
    #print(listOfReading_FoodRestriction)
    if (save_table(db,listOfReading_FoodRestriction) == 0):
        arr_tables_inserted.append(FoodRestriction)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(FoodRestriction)
    count_tables_inserted += 1

    # #------------------------------------------------

    listOfReading_Licensed_Medicine = read_and_format_catalogs_licensed_medicine()
    print("-"*30)
    #print(listOfReading_Licensed_Medicine)
    if (save_table(db,listOfReading_Licensed_Medicine) == 0):
        arr_tables_inserted.append(LicensedMedicine)
        count_tables_inserted += 1 
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(LicensedMedicine)
    count_tables_inserted += 1

    # #------------------------------------------------

    listOfReading_pathological_background = read_and_format_catalogs_pathological_background()
    print("-"*30)
    #print(listOfReading_pathological_background)
    if (save_table(db,listOfReading_pathological_background) == 0):
        arr_tables_inserted.append(PathologicalBackground)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(PathologicalBackground)
    count_tables_inserted += 1

    # #------------------------------------------------

    listOfReading_background_family = read_and_format_catalogs_pathological_background_family()
    print("-"*30)
    #print(listOfReading_background_family)
    if (save_table(db,listOfReading_background_family) == 0):
        arr_tables_inserted.append(PathologicalBackgroundFamily)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(PathologicalBackgroundFamily)
    count_tables_inserted += 1

    # #------------------------------------------------

    listOfReading_auth_group = read_and_format_auth_group()
    print("-"*30)
    #print(listOfReading_auth_group)
    if (save_table(db,listOfReading_auth_group) == 0):
        arr_tables_inserted.append(Role)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Role)
    count_tables_inserted += 1

    # #------------------------------------------------

    with open('csv/staff_staff.csv', 'r') as archivo_entrada, open('csv/limpio_staff_staff.csv', 'w') as archivo_salida:
        for linea in archivo_entrada:
            linea_limpia = linea.replace("\\N", "")#strip('\N')  # Elimina saltos de línea al principio y al final
            archivo_salida.write(linea_limpia)  # Vuelve a agregar una nueva línea al final  

    listOfReading_auth_campercontrol_user = read_and_format_auth_campercontrol_user()
    print("-"*30)

    # print(listOfReading_auth_campercontrol_user)
    if (save_table(db,listOfReading_auth_campercontrol_user) == 0):
        arr_tables_inserted.append(User)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(User)
    count_tables_inserted += 1

    # #------------------------------------------------

    listOfReading_campers_school = read_and_format_campers_school()
    print("-"*30)
    #print(listOfReading_campers_school)
    if (save_table(db,listOfReading_campers_school) == 0):
        arr_tables_inserted.append(School)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(School)
    count_tables_inserted += 1

    # #------------------------------------------------

    listOfReading_campers_parent = read_and_format_campers_parent()
    print("-"*30)
    #print(listOfReading_campers_parent)

    if (save_table(db,listOfReading_campers_parent) == 0):
        arr_tables_inserted.append(Parent)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Parent)
    count_tables_inserted += 1

    # #------------------------------------------------

    listOfReading_campers_camperrecords = read_and_format_campers_camperrecords()
    if (save_table(db,listOfReading_campers_camperrecords) == 0):
        arr_tables_inserted.append(CamperRecord)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperRecord)
    count_tables_inserted += 1

    # #------------------------------------------------

    with open('csv/campers_camper.csv', 'r') as archivo_entrada, open('csv/limpio_campers_camper.csv', 'w') as archivo_salida:
        for linea in archivo_entrada:
            linea_limpia = linea.replace("\\N", "")#strip('\N')  # Elimina saltos de línea al principio y al final
            archivo_salida.write(linea_limpia)  # Vuelve a agregar una nueva línea al final

    listOfReading_campers_camper = read_and_format_campers_camper()

    # print("/\\"*30)
    # print(arr_error)

    if (save_table(db,listOfReading_campers_camper) == 0):
        arr_tables_inserted.append(Camper)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Camper)
    count_tables_inserted += 1

    # # #------------------------------------------------

    listOfReading_campers_camper_food_restriction = read_and_format_campers_camper_food_restriction()
    if (save_table(db,listOfReading_campers_camper_food_restriction) == 0):
        arr_tables_inserted.append(CamperFoodRestriction)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperFoodRestriction)
    count_tables_inserted += 1

    # # #------------------------------------------------

    listOfReading_campers_camper_authorized_drugs = read_and_format_campers_camper_authorized_drugs()
    if (save_table(db,listOfReading_campers_camper_authorized_drugs) == 0):
        arr_tables_inserted.append(CamperLicensedMedicine)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperLicensedMedicine)
    count_tables_inserted += 1

    # # #------------------------------------------------

    listOfReading_campers_camper_pathological_background_family = read_and_format_campers_camper_pathological_background_family()
    if (save_table(db,listOfReading_campers_camper_pathological_background_family) == 0):
        arr_tables_inserted.append(CamperPathologicalBackgroundFamily)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperPathologicalBackgroundFamily)
    count_tables_inserted += 1

    # # #------------------------------------------------

    listOfReading_campers_camper_pathological_background = read_and_format_campers_camper_pathological_background()
    if (save_table(db,listOfReading_campers_camper_pathological_background) == 0):
        arr_tables_inserted.append(CamperPathologicalBackground)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperPathologicalBackground)
    count_tables_inserted += 1

    # # #------------------------------------------------

    listOfReading_campers_camper_vaccines = read_and_format_campers_camper_vaccines()
    if (save_table(db,listOfReading_campers_camper_vaccines) == 0):
        arr_tables_inserted.append(CamperVaccine)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperVaccine)
    count_tables_inserted += 1

    # # #------------------------------------------------

    with open('csv/camps_location.csv', 'r') as archivo_entrada, open('csv/limpio_camps_location.csv', 'w') as archivo_salida:
        for linea in archivo_entrada:
            linea_limpia = linea.replace("\\N", "")#strip('\N')  # Elimina saltos de línea al principio y al final
            archivo_salida.write(linea_limpia)  # Vuelve a agregar una nueva línea al final

    listOfReading_camps_location = read_and_format_camps_location()
    if (save_table(db,listOfReading_camps_location) == 0):
        arr_tables_inserted.append(Location)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Location)
    count_tables_inserted += 1

    # # #------------------------------------------------

    listOfReading_camps_season = read_and_format_camps_season()
    if (save_table(db,listOfReading_camps_season) == 0):
        arr_tables_inserted.append(Season)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Season)
    count_tables_inserted += 1

    # # #------------------------------------------------

    with open('csv/camps_camp.csv', 'r') as archivo_entrada, open('csv/limpio_camps_camp.csv', 'w') as archivo_salida:
        for linea in archivo_entrada:
            linea_limpia = linea.replace("\\N", "")#strip('\N')  # Elimina saltos de línea al principio y al final
            archivo_salida.write(linea_limpia)  # Vuelve a agregar una nueva línea al final

    listOfReading_camps_camp = read_and_format_camps_camp()
    if (save_table(db,listOfReading_camps_camp) == 0):
        arr_tables_inserted.append(Camp)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Camp)
    count_tables_inserted += 1

    # # #------------------------------------------------

    listOfReading_camps_camp_payments_accounts = read_and_format_camps_camp_payments_accounts()
    if (save_table(db,listOfReading_camps_camp_payments_accounts) == 0):
        arr_tables_inserted.append(CampPaymentAccount)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CampPaymentAccount)
    count_tables_inserted += 1

    # # # #------------------------------------------------

    listOfReading_camps_campextracharge = read_and_format_camps_campextracharge()
    if (save_table(db,listOfReading_camps_campextracharge) == 0):
        arr_tables_inserted.append(CampExtraCharge)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CampExtraCharge)
    count_tables_inserted += 1

    # # #------------------------------------------------

    listOfReading_camps_checkpoint = read_and_format_camps_checkpoint()
    if (save_table(db,listOfReading_camps_checkpoint) == 0):
        arr_tables_inserted.append(CampCheckpoint)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CampCheckpoint)
    count_tables_inserted += 1

    # # #------------------------------------------------

    listOfReading_camps_checkpointcamper = read_and_format_camps_checkpointcamper()
    if (save_table(db,listOfReading_camps_checkpointcamper) == 0):
        arr_tables_inserted.append(CamperCheckpoint)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperCheckpoint)
    count_tables_inserted += 1

    # # #------------------------------------------------

    listOfReading_camps_extraquestion = read_and_format_camps_extraquestion()
    if (save_table(db,listOfReading_camps_extraquestion) == 0):
        arr_tables_inserted.append(CampExtraQuestion)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CampExtraQuestion)
    count_tables_inserted += 1
    
    # # #------------------------------------------------

    listOfReading_campers_extraanswers = read_and_format_campers_extraanswers()
    if (save_table(db,listOfReading_campers_extraanswers) == 0):
        arr_tables_inserted.append(CamperExtraAnswer)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperExtraAnswer)
    count_tables_inserted += 1
    
    # # #------------------------------------------------

    with open('csv/campers_campercomment.csv', 'r') as archivo_entrada, open('csv/limpio_campers_campercomment.csv', 'w') as archivo_salida:
        for linea in archivo_entrada:
            linea_limpia = linea.replace("\\N", "")#strip('\N')  # Elimina saltos de línea al principio y al final
            archivo_salida.write(linea_limpia)  # Vuelve a agregar una nueva línea al final    

    listOfReading_campers_campercomment = read_and_format_campers_campercomment()
    if (save_table(db,listOfReading_campers_campercomment) == 0):
        arr_tables_inserted.append(CamperComment)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperComment)
    count_tables_inserted += 1

    # # #------------------------------------------------   

    listOfReading_camps_camperincamp = read_and_format_camps_camperincamp()
    if (save_table(db,listOfReading_camps_camperincamp) == 0):
        arr_tables_inserted.append(CamperInCamp)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperInCamp)
    count_tables_inserted += 1

    # # #------------------------------------------------   

    listOfReading_camps_training = read_and_format_camps_training()
    if (save_table(db,listOfReading_camps_training) == 0):
        arr_tables_inserted.append(Training)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Training)
    count_tables_inserted += 1

    # # #------------------------------------------------   

    listOfReading_camps_training = read_and_format_camps_trainingevent()
    if (save_table(db,listOfReading_camps_training) == 0):
        arr_tables_inserted.append(TrainingEvent)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(TrainingEvent)
    count_tables_inserted += 1

    # # #------------------------------------------------   

    listOfReading_camps_campdiscount = read_and_format_camps_campdiscount()
    if (save_table(db,listOfReading_camps_campdiscount) == 0):
        arr_tables_inserted.append(CampDiscount)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CampDiscount)
    count_tables_inserted += 1

    # # #------------------------------------------------   

    listOfReading_staff_userrecords = read_and_format_staff_userrecords()
    if (save_table(db,listOfReading_staff_userrecords) == 0):
        arr_tables_inserted.append(StaffRecord)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(StaffRecord)
    count_tables_inserted += 1

    # # #------------------------------------------------   

    with open('csv/staff_staff.csv', 'r') as archivo_entrada, open('csv/limpio_staff_staff.csv', 'w') as archivo_salida:
        for linea in archivo_entrada:
            linea_limpia = linea.replace("\\N", "")#strip('\N')  # Elimina saltos de línea al principio y al final
            archivo_salida.write(linea_limpia)  # Vuelve a agregar una nueva línea al final  

    listOfReading_staff_staff = read_and_format_staff_staff()
    if (save_table(db,listOfReading_staff_staff) == 0):
        arr_tables_inserted.append(Staff)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Staff)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    with open('csv/camps_staffincamp.csv', 'r') as archivo_entrada, open('csv/limpio_camps_staffincamp.csv', 'w') as archivo_salida:
        for linea in archivo_entrada:
            linea_limpia = linea.replace("\\N", "")#strip('\N')  # Elimina saltos de línea al principio y al final
            archivo_salida.write(linea_limpia + "\n")  # Vuelve a agregar una nueva línea al final  

    listOfReading_camps_staffincamp = read_and_format_camps_staffincamp()
    if (save_table(db,listOfReading_camps_staffincamp) == 0):
        arr_tables_inserted.append(StaffInCamp)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(StaffInCamp)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    listOfReading_camps_staffintraining = read_and_format_camps_staffintraining()
    if (save_table(db,listOfReading_camps_staffintraining) == 0):
        arr_tables_inserted.append(StaffInTraining)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(StaffInTraining)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    listOfReading_staff_staff_food_restriction = read_and_format_staff_staff_food_restriction()
    if (save_table(db,listOfReading_staff_staff_food_restriction) == 0):
        arr_tables_inserted.append(StaffFoodRestriction)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(StaffFoodRestriction)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    listOfReading_staff_staff_vaccines = read_and_format_staff_staff_vaccines()
    if (save_table(db,listOfReading_staff_staff_vaccines) == 0):
        arr_tables_inserted.append(StaffVaccine)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(StaffVaccine)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    listOfReading_staff_staffcomment = read_and_format_staff_staffcomment()
    if (save_table(db,listOfReading_staff_staffcomment) == 0):
        arr_tables_inserted.append(StaffComment)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(StaffComment)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    listOfReading_trophy_trophy = read_and_format_trophy_trophy()
    if (save_table(db,listOfReading_trophy_trophy) == 0):
        arr_tables_inserted.append(Trophy)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Trophy)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    ##Season
    listOfReading_trophy_trophystaff = read_and_format_trophy_trophystaff()
    if (save_table(db,listOfReading_trophy_trophystaff) == 0):
        arr_tables_inserted.append(TrophySeason)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(TrophySeason)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    listOfReading_trophy_trophystaff_holder = read_and_format_trophy_trophystaff_holder()
    if (save_table(db,listOfReading_trophy_trophystaff_holder) == 0):
        arr_tables_inserted.append(TrophyStaff)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(TrophyStaff)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    listOfReading_mailing_emailtemplate = read_and_format_mailing_emailtemplate()
    if (save_table(db,listOfReading_mailing_emailtemplate) == 0):
        arr_tables_inserted.append(EmailTemplate)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(EmailTemplate)
    count_tables_inserted += 1

    # # #------------------------------------------------ 
    
    with open('csv/mailing_campaign.csv', 'r') as archivo_entrada, open('csv/limpio_mailing_campaign.csv', 'w') as archivo_salida:
        for linea in archivo_entrada:
            linea_limpia = linea.replace("\\N", "")#strip('\N')  # Elimina saltos de línea al principio y al final
            archivo_salida.write(linea_limpia + "\n")  # Vuelve a agregar una nueva línea al final  

    listOfReading_mailing_campaign = read_and_format_mailing_campaign()
    if (save_table(db,listOfReading_mailing_campaign) == 0):
        arr_tables_inserted.append(Campaign)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Campaign)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    listOfReading_mailing_campaign_campers = read_and_format_mailing_campaign_campers()
    if (save_table(db,listOfReading_mailing_campaign_campers) == 0):
        arr_tables_inserted.append(CamperCampaign)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperCampaign)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    listOfReading_mailing_campaign_staff = read_and_format_mailing_campaign_staff()
    if (save_table(db,listOfReading_mailing_campaign_staff) == 0):
        arr_tables_inserted.append(StaffCampaign)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(StaffCampaign)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    listOfReading_payments_paymentmethod = read_and_format_payments_paymentmethod()
    if (save_table(db,listOfReading_payments_paymentmethod) == 0):
        arr_tables_inserted.append(PaymentMethod)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(PaymentMethod)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    listOfReading_payments_paymenttransactiontype = read_and_format_payments_paymenttransactiontype()
    if (save_table(db,listOfReading_payments_paymenttransactiontype) == 0):
        arr_tables_inserted.append(PaymentTransactionType)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(PaymentTransactionType)
    count_tables_inserted += 1

    # # #------------------------------------------------    

    with open('csv/payments_payment.csv', 'r') as archivo_entrada, open('csv/limpio_payments_payment.csv', 'w') as archivo_salida:
        for linea in archivo_entrada:
            linea_limpia = linea.replace("\\N", "")#strip('\N')  # Elimina saltos de línea al principio y al final
            archivo_salida.write(linea_limpia + "\n")  # Vuelve a agregar una nueva línea al final  

    listOfReading_payments_payment = read_and_format_payments_payment()
    if (save_table(db,listOfReading_payments_payment) == 0):
        arr_tables_inserted.append(Payment)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(Payment)
    count_tables_inserted += 1

    # # #------------------------------------------------     

    listOfReading_payments_camperextracharge = read_and_format_payments_camperextracharge()
    if (save_table(db,listOfReading_payments_camperextracharge) == 0):
        arr_tables_inserted.append(CamperExtraCharge)
        count_tables_inserted += 1
        truncate_database(db,count_tables_inserted,arr_tables_inserted)
        return []
    arr_tables_inserted.append(CamperExtraCharge)
    count_tables_inserted += 1

    # print(result)
    # for i in result:
    #     print(i)

    print(f'arr_tables_inserted {arr_tables_inserted}')
    print(f'count_tables_inserted {count_tables_inserted}')


    return []


def buscar_campo_y_nombre_seq(db,nombre_tabla):
    campo = ""
    nombre_seq = ""
    try:
        txt = f"""SELECT column_name, column_default 
                FROM information_schema.columns
                WHERE table_name = '{nombre_tabla}' AND column_default LIKE 'nextval%' """
        #print(txt)
        sql_seq = text(txt)
        #print(sql_seq)
        result = db.execute(sql_seq)
        #print(result)
        
        for row in result:
            print(row)
            campo = row[0]
            nombre_seq = str(row[1]).replace("nextval('","").replace("'::regclass)","")
        print(campo)
        print(nombre_seq)

    except Exception as ex:
        result = 0
        print(f"Error en busqueda de sequencias {ex}")
    return campo,nombre_seq


def buscar_maximo_id_by_tabla(db,nombre_tabla,nombre_campo):
    numero_max = 1
    try:
        txt = f"""select max({nombre_campo}) from "{nombre_tabla}" """ 
        #print(txt)
        sql_max = text(txt)
        #print(sql_seq)
        result = db.execute(sql_max)
        #print(result)
        
        for row in result:
            print(row)
            numero_max = row[0]
        print(numero_max)

    except Exception as ex:
        result = 0
        print(f"Error en max de registros {ex}")
    return numero_max


def alterar_sequencia(db,nombre_seq,numero_max):
    #numero_max = 1
    try:
        txt = f"ALTER SEQUENCE {nombre_seq} RESTART WITH {numero_max}" 
        print(txt)
        sql_act_seq = text(txt)
        #print(sql_seq)
        result = db.execute(sql_act_seq)
        print(result)
        db.commit()
        
        # for row in result:
        #     print(row)
        #     numero_max = row[0]
        # print(numero_max)

    except Exception as ex:
        result = 0
        print(f"Error en max de registros {ex}")
    return 0



@timer
def buscar_ajustar_secuencias(db):

    tablas = [
        "camps_training",
        "staff_userrecords",
        "payments_paymentmethod",
        "payments_paymenttransactiontype",
        "catalogs_pathological_background_family",
        "staff_staff",
        "camps_staffincamp",
        "staff_staff_vaccines",
        "campers_extraanswers",
        "payments_payment",
        "camps_campdiscount",
        "camps_camperincamp",
        "campers_camper_licensed_medicine",
        "campers_camper_pathological_background",
        "campers_camper_pathological_background_family",
        "staff_staffcomment",
        "camps_staffintraining",
        "staff_staff_food_restriction",
        "campers_parent",
        "catalogs_constant",
        "campers_camper",
        "camps_checkpointcamper",
        "payments_camperextracharge",
        "mailing_emailtemplate",
        "campers_campercomment",
        "catalogs_vaccine",
        "mailing_school_campaign",
        "mailing_staff_campaign",
        "trophy_trophystaff_holder",
        "camps_extraquestion",
        "campers_camper_vaccines",
        "catalogs_staff_role",
        "role",
        "camps_location",
        "camps_season",
        "camps_camp_payments_accounts",
        "catalogs_food_restriction",
        "catalogs_licensed_medicine",
        "campers_school",
        "campers_camperrecords",
        "trophy_trophystaff",
        "catalogs_payment_account",
        "permission",
        "user",
        "catalogs_pathological_background",
        "trophy_trophy",
        "mailing_campaign",
        "campers_camper_food_restriction",
        "camps_trainingevent",
        "mailing_camper_campaign",
        "catalogs_currency",
        "camps_camp",
        "camps_campextracharge",
        "camps_checkpoint"
        ]
    
    for nombre_tabla in tablas:
        print(nombre_tabla + " ...")

        #nombre_tabla = 'camps_camperincamp'

        campo, nombre_seq = buscar_campo_y_nombre_seq(db,nombre_tabla)

        if nombre_seq == "":
            continue

        numero_max = buscar_maximo_id_by_tabla(db,nombre_tabla,campo)

        # print(type(numero_max))
        # print(type(None))

        if numero_max is None:
            continue

        print(numero_max + 1)

        resultado = alterar_sequencia(db,nombre_seq,numero_max+1)

