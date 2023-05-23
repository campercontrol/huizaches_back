import jinja2
import pdfkit
from utils.barcode_tools import generate_code128, generate_code128_no_fotter
from utils.image_tools import img_to_base_64
#from fastapi.templating impor Jin

def generar_pdf_bracelete():
    
    code = "200798"
    ruta1 = generate_code128_no_fotter(code) 
    barcode_64 = "data:image/png;base64," + img_to_base_64(f"{ruta1}").decode("utf-8")
    logo_64 = "data:image/png;base64," + img_to_base_64("media/templates_pdf/logo/kincamp_logo_color.png").decode("utf-8")

    context = {
        "name":"AILYN ROSALÉ CALDERÓN TORRES",
        "school":"Escuela Prueba",
        "camping":"PRUEBA 1",
        "barcode_img":barcode_64,
        "barcode_code":code,        
        "blood_type":"A+",
        "alergies":"NO",
        "other_alergies":"NO",
        "prohibed_foo":"NO",
        "logo_img":logo_64,
        }
    
    template_loader = jinja2.FileSystemLoader('media/templates_pdf/')
    template_env= jinja2.Environment(loader = template_loader)

    html_info_camper = 'bracelete.html' #Nombre del template que se usa el html 

    template = template_env.get_template(html_info_camper)
 
    html_content = template.render(context) #Renderiza los datos en el html

    print("//////////")
    print(html_content)

    #Try para verificar paquete de libreria que permite usar la generacion de html a pdf 
    try:
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        output_pdf = "media/bracelete.pdf" #Nombre y ubicacion del archivo ya en pdf
        pdfkit.from_string(html_content, output_pdf, configuration=config)
         
    except OSError:
    #not present in PATH
        print("path_not_found")


def generar_pdf_bracelete_multiple():
    
    code = "200798"
    ruta1 = generate_code128_no_fotter(code) 
    barcode_64 = "data:image/png;base64," + img_to_base_64(f"{ruta1}").decode("utf-8")
    logo_64 = "data:image/png;base64," + img_to_base_64("media/templates_pdf/logo/kincamp_logo_color.png").decode("utf-8")

    context = {
        "name":"AILYN ROSALÉ CALDERÓN TORRES",
        "school":"Escuela Prueba",
        "camping":"PRUEBA 1",
        "barcode_img":barcode_64,
        "barcode_code":code,        
        "blood_type":"A+",
        "alergies":"NO",
        "other_alergies":"NO",
        "prohibed_foo":"NO",
        "logo_img":logo_64,
        }
    
    list_of_context = {
        "list_bracelet" : [
            context,
            context,
            context
        ]
    }
    
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
        pdfkit.from_string(html_content, output_pdf, configuration=config)
         
    except OSError:
    #not present in PATH
        print("path_not_found")


