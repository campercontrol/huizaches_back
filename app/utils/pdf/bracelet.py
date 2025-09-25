import jinja2
import pdfkit
from utils.barcode_tools import generate_code128, generate_code128_no_fotter
from utils.image_tools import img_to_base_64
#from fastapi.templating impor Jin

def generar_pdf_bracelete(list_campers, camp_name):
    
    #code = "200798"
    #ruta1 = generate_code128_no_fotter(code) 
    #barcode_64 = "data:image/png;base64," + img_to_base_64(f"{ruta1}").decode("utf-8")
    logo_64 = "data:image/png;base64," + img_to_base_64("media/templates_pdf/logo/kincamp_logo_color.png").decode("utf-8")

    list_b = []
    for camper in list_campers:
        code =  str(camper["camper_id"]).zfill(6)
        ruta1 = generate_code128_no_fotter(code) 
        barcode_64 = "data:image/png;base64," + img_to_base_64(f"{ruta1}").decode("utf-8")
        context = {
            "name":  camper["name"],
            "school": camper["school"],
            "camping": camp_name,
            "barcode_img":barcode_64,
            "barcode_code":code,        
            "blood_type": camper["blood_type"],
            "alergies": camper["alergies"],
            "other_alergies": camper["other_alergies"],
            "prohibed_foo":  camper["prohibed_foo"],
            "groupings": camper["groupings"],
            "logo_img":logo_64,
            }
        list_b.append(context)

    list_context = {
        "list_bracelet" : list_b
    }


    #context = {
    #    "name":"AILYN ROSALÉ CALDERÓN TORRES",
    #    "school":"Escuela Prueba",
    #    "camping":"PRUEBA 1",
    #    "barcode_img":barcode_64,
    #    "barcode_code":code,        
    #    "blood_type":"A+",
    #    "alergies":"NO",
    #    "other_alergies":"NO",
    #    "prohibed_foo":"NO",
    #    "logo_img":logo_64,
    #    }
    
    template_loader = jinja2.FileSystemLoader('media/templates_pdf/')
    template_env= jinja2.Environment(loader = template_loader)

    html_info_camper = 'bracelete.html' #Nombre del template que se usa el html 

    template = template_env.get_template(html_info_camper)
 
    html_content = template.render(list_context) #Renderiza los datos en el html

    # print(html_content)

    #Try para verificar paquete de libreria que permite usar la generacion de html a pdf 
    
    output_pdf = "media/bracelete.pdf" #Nombre y ubicacion del archivo ya en pdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    pdfkit.from_string(
        html_content, 
        output_pdf, 
        configuration=config,
        options = {
            'page-height': '11in',
            'page-width': '1in',
            'margin-top': '0',
            'margin-right': '0',
            'margin-bottom': '0',
            'margin-left': '0',
            'encoding': "UTF-8"
            }
        )
    return output_pdf


def generar_pdf_bracelete_multiple(list_campers, camp_name):
    
    code = "200798"
    ruta1 = generate_code128_no_fotter(code) 
    barcode_64 = "data:image/png;base64," + img_to_base_64(f"{ruta1}").decode("utf-8")
    logo_64 = "data:image/png;base64," + img_to_base_64("media/templates_pdf/logo/kincamp_logo_color.png").decode("utf-8")

    list_b = []
    for camper in list_campers:
        code =  str(getattr(camper, "camper_id")).zfill(6)
        ruta1 = generate_code128_no_fotter(code) 
        barcode_64 = "data:image/png;base64," + img_to_base_64(f"{ruta1}").decode("utf-8")
        
        context = {
            "name":  getattr(camper, "name"),
            "school": getattr(camper, "school"),
            "camping": camp_name,
            "barcode_img":barcode_64,
            "barcode_code":code,        
            "blood_type": getattr(camper, "blood_type"),
            "alergies": getattr(camper, "alergies"),
            "other_alergies": getattr(camper, "other_alergies"),
            "prohibed_foo":  getattr(camper, "prohibed_foo"),
            "logo_img":logo_64,
            }
        list_b.append(context)
    
    list_of_context = {
        "list_bracelet" : list_b
    }

    print(list_of_context)
    
    template_loader = jinja2.FileSystemLoader('media/templates_pdf/')
    template_env= jinja2.Environment(loader = template_loader)

    html_info_camper = 'bracelete_multiple.html' #Nombre del template que se usa el html 

    template = template_env.get_template(html_info_camper)
 
    html_content = template.render(list_of_context) #Renderiza los datos en el html

    print("//////////")
    print(html_content)

    #Try para verificar paquete de libreria que permite usar la generacion de html a pdf 
    try:
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        output_pdf = "media/bracelete_multiple.pdf" #Nombre y ubicacion del archivo ya en pdf
        pdfkit.from_string(
            html_content, 
            output_pdf, 
            configuration=config,
            options = {
                'page-height': '279.4mm',
                'page-width': '215.9mm',
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
    return output_pdf


