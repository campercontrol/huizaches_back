import os
import jinja2
import pdfkit
from datetime import datetime
from utils.barcode_tools import generate_code128, generate_code128_no_fotter
from utils.image_tools import img_to_base_64

from PyPDF2 import PdfMerger

#from fastapi.templating impor Jin

CAMP_LOGO_BLACK_FILE_NAME = os.getenv("CAMP_LOGO_BLACK_FILE_NAME")
def generar_pdf_info_camping():

    ruta1 = generate_code128("200798") #Generar codigo de barras
    #ruta2 = generate_code128_no_fotter("200798")

    #Traer imagen en base64
    barcode_64 = "data:image/png;base64," + img_to_base_64(f"{ruta1}").decode("utf-8")
    logo_64 = "data:image/png;base64," + img_to_base_64(f"media/assets/logos/{CAMP_LOGO_BLACK_FILE_NAME}").decode("utf-8")

    context = {
        "logo": logo_64,
        "nombre_camping":"Merici 4to. primaria Abril 2023",
        "barcode": barcode_64,
        "nombre_camper":"Jorge A",
        "apellido_paterno_camper":"Almazan",
        "apellido_materno_camper":"Mendez",
        "escuela_camper":"Calmecac",
        "fecha_nacimiento_camper":"20-07-98",
        "email_camper":"almazanmendez@hotmail.com",
        "gender":"M",
        "grade":"Ing",
        "weidth":"110 Kg",
        "height":"171",
        "blood_type":"O+",
        "insurance":"Patito",
        "camper_diseases":"no",
        "camper_nocturnal_disturbances":"no",
        "camper_fear":"no",
        "camper_medication":"no",
        "camper_alergies":"no",
        "camper_other_alergies":"no",
        "camper_prohibed_foods":"no",
        "camper_especial_alimentation":"no",
        "camper_vaccines":"no",
        "camper_extra_questions":"no",
        "camper_extra_charge":"no",
        "camper_comments":"no",

        "princ_name_tuto":"",
        "princ_email_tuto":"",
        "princ_celular_tuto":"",
        "princ_tel_casa_tuto":"",
        "princ_tel_ofc_tuto":"",

        "sec_name_tuto":"",
        "sec_email_tuto":"",
        "sec_celular_tuto":"",
        "sec_tel_casa_tuto":"",
        "sec_tel_ofc_tuto":"",

        "emer_name_tuto":"",
        "emer_parent_tuto":"",
        "emer_celular_tuto":"",
        "emer_tel_casa_tuto":"",

        "address":"Chihuahua 230, Col. Roma, CP. 06700, CDMX",
        "contact_email":"info@kincamp.com",
        "creation_date":datetime.now().strftime('%Y/%m/%d')
        
        }
    
    template_loader = jinja2.FileSystemLoader('media/templates_pdf/')
    template_env= jinja2.Environment(loader = template_loader)

    html_info_camper = 'camper_info.html' #Nombre del template que se usa el html 

    template = template_env.get_template(html_info_camper)
 
    html_content = template.render(context) #Renderiza los datos en el html

    print("//////////")
    print(html_content)

    #Try para verificar paquete de libreria que permite usar la generacion de html a pdf 
    try:
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        output_pdf = "media/camping_info.pdf" #Nombre y ubicacion del archivo ya en pdf
        pdfkit.from_string(
            html_content, 
            output_pdf, 
            configuration=config , 
            options = {
                'page-size': 'Letter',
                'margin-top': '0',
                'margin-right': '0',
                'margin-bottom': '0',
                'margin-left': '0',
                'encoding': "UTF-8"
                }
            )
           
    except OSError:
    #not present in PATH
        print("path_not_found")

    # config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
    return output_pdf


def generar_pdf_info_camping_multiple():

    ruta1 = generate_code128("200798") #Generar codigo de barras
    #ruta2 = generate_code128_no_fotter("200798")

    #Traer imagen en base64
    barcode_64 = "data:image/png;base64," + img_to_base_64(f"{ruta1}.png").decode("utf-8")
    logo_64 = "data:image/png;base64," + img_to_base_64(f"media/assets/logos/{CAMP_LOGO_BLACK_FILE_NAME}").decode("utf-8")

    context = {
        "logo": logo_64,
        "nombre_camping":"Merici 4to. primaria Abril 2023",
        "barcode": barcode_64,
        "nombre_camper":"Jorge A",
        "apellido_paterno_camper":"Almazan",
        "apellido_materno_camper":"Mendez",
        "escuela_camper":"Calmecac",
        "fecha_nacimiento_camper":"20-07-98",
        "email_camper":"almazanmendez@hotmail.com",
        "gender":"M",
        "grade":"Ing",
        "weidth":"110 Kg",
        "height":"171",
        "blood_type":"O+",
        "insurance":"Patito",
        "camper_diseases":"no",
        "camper_nocturnal_disturbances":"no",
        "camper_fear":"no",
        "camper_medication":"no",
        "camper_alergies":"no",
        "camper_other_alergies":"no",
        "camper_prohibed_foods":"no",
        "camper_especial_alimentation":"no",
        "camper_vaccines":"no",
        "camper_extra_questions":"no",
        "camper_extra_charge":"no",
        "camper_comments":"no",

        "princ_name_tuto":"",
        "princ_email_tuto":"",
        "princ_celular_tuto":"",
        "princ_tel_casa_tuto":"",
        "princ_tel_ofc_tuto":"",

        "sec_name_tuto":"",
        "sec_email_tuto":"",
        "sec_celular_tuto":"",
        "sec_tel_casa_tuto":"",
        "sec_tel_ofc_tuto":"",

        "emer_name_tuto":"",
        "emer_parent_tuto":"",
        "emer_celular_tuto":"",
        "emer_tel_casa_tuto":"",
        
        "address":"Chihuahua 230, Col. Roma, CP. 06700, CDMX",
        "contact_email":"info@kincamp.com",
        "creation_date":datetime.now().strftime('%Y/%m/%d')
        }
    
    template_loader = jinja2.FileSystemLoader('media/templates_pdf/')
    template_env= jinja2.Environment(loader = template_loader)

    html_info_camper = 'camper_info.html' #Nombre del template que se usa el html 

    template = template_env.get_template(html_info_camper)
 
    html_content = template.render(context) #Renderiza los datos en el html

    print("//////////")
    print(html_content)

    list_html_contents = ""

    for i in range(200):
        list_html_contents += html_content + '<br>'

    #Try para verificar paquete de libreria que permite usar la generacion de html a pdf 
    try:
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        output_pdf = "media/camping_info_multiple.pdf" #Nombre y ubicacion del archivo ya en pdf
        pdfkit.from_string(
            list_html_contents, 
            output_pdf, 
            configuration=config,
            options = {
                'page-size': 'Letter',
                'margin-top': '0',
                'margin-right': '0',
                'margin-bottom': '0',
                'margin-left': '0',
                'encoding': "UTF-8"
                }
            )
         
    except OSError:
    #not present in PATH
        print("path_not_found")


def generar_pdf_info_camping_multiple_merge_files():
    ruta1 = generate_code128("200798") #Generar codigo de barras
    #ruta2 = generate_code128_no_fotter("200798")

    #Traer imagen en base64
    barcode_64 = "data:image/png;base64," + img_to_base_64(f"{ruta1}").decode("utf-8")
    logo_64 = "data:image/png;base64," + img_to_base_64(f"media/assets/logos/{CAMP_LOGO_BLACK_FILE_NAME}").decode("utf-8")

    context = {
        "logo": logo_64,
        "nombre_camping":"Merici 4to. primaria Abril 2023",
        "barcode": barcode_64,
        "nombre_camper":"Jorge A",
        "apellido_paterno_camper":"Almazan",
        "apellido_materno_camper":"Mendez",
        "escuela_camper":"Calmecac",
        "fecha_nacimiento_camper":"20-07-98",
        "email_camper":"almazanmendez@hotmail.com",
        "gender":"M",
        "grade":"Ing",
        "weidth":"110 Kg",
        "height":"171",
        "blood_type":"O+",
        "insurance":"Patito",
        "camper_diseases":"no",
        "camper_nocturnal_disturbances":"no",
        "camper_fear":"no",
        "camper_medication":"no",
        "camper_alergies":"no",
        "camper_other_alergies":"no",
        "camper_prohibed_foods":"no",
        "camper_especial_alimentation":"no",
        "camper_vaccines":"no",
        "camper_extra_questions":"no",
        "camper_extra_charge":"no",
        "camper_comments":"no",

        "princ_name_tuto":"",
        "princ_email_tuto":"",
        "princ_celular_tuto":"",
        "princ_tel_casa_tuto":"",
        "princ_tel_ofc_tuto":"",

        "sec_name_tuto":"",
        "sec_email_tuto":"",
        "sec_celular_tuto":"",
        "sec_tel_casa_tuto":"",
        "sec_tel_ofc_tuto":"",

        "emer_name_tuto":"",
        "emer_parent_tuto":"",
        "emer_celular_tuto":"",
        "emer_tel_casa_tuto":"",
        
        "address":"Chihuahua 230, Col. Roma, CP. 06700, CDMX",
        "contact_email":"info@kincamp.com",
        "creation_date":datetime.now().strftime('%Y/%m/%d')
        }
    
    list_context = []

    for i in range(200):
        list_context.append(context)
    
    #list_context = [context,context,context,context,context]

    template_loader = jinja2.FileSystemLoader('media/templates_pdf/')
    template_env= jinja2.Environment(loader = template_loader)

    html_info_camper = 'camper_info.html' #Nombre del template que se usa el html 

    template = template_env.get_template(html_info_camper)

    list_output_pdf = []

    for indice,elemento in enumerate(list_context):

        html_content = template.render(elemento) #Renderiza los datos en el html

        #Try para verificar paquete de libreria que permite usar la generacion de html a pdf 
        try:
            config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
            output_pdf = f"media/camping_info_{indice}.pdf" #Nombre y ubicacion del archivo ya en pdf
            pdfkit.from_string(html_content, output_pdf, configuration=config)
            list_output_pdf.append(output_pdf)
            
        except OSError:
        #not present in PATH
            print("path_not_found")

    #merge Pdf
    merger = PdfMerger()

    for pdf_file in list_output_pdf:
        #Append PDF files
        merger.append(pdf_file)

    #Write out the merged PDF file
    merger.write("media/merged_camping_info.pdf")
    merger.close()
    return "media/merged_camping_info.pdf"