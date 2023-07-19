import jinja2
import pdfkit
from utils.barcode_tools import generate_code128, generate_code128_no_fotter
from utils.image_tools import img_to_base_64
#from fastapi.templating impor Jin

def generar_pdf_baucher(context):

    #logo_64 = "data:image/png;base64," + img_to_base_64("media/templates_pdf/logo/kincamp_logo_color.png").decode("utf-8")

    #context = {
    #    "name_camping": "Ailyn Rosalé Calderón",
    #    "camping_name": "Prueba 1",
    #    "amount_total":"$11,000.00",
    #    "logo":logo_64,
    #    "information_accounts":[
    #        {
    #        "bank":"BBVA",
    #        "name_reference":"Angela Patricia Avila Rojas",
    #        "account_number":"0199909435",
    #        "clabe":"012180001999094351",
    #        },
    #         {
    #        "bank":"BBVA",
    #        "name_reference":"Angela Patricia Avila Rojas",
    #        "account_number":"0199909435",
    #        "clabe":"012180001999094351",
    #        }
    #    ],
    #    "pay_reference":"0044448",
    #    "more_info":"patito.com",
    #    "email":"pagos@kincamp.com"
    #    }
    
    template_loader = jinja2.FileSystemLoader('media/templates_pdf/')
    template_env= jinja2.Environment(loader = template_loader)

    html_info_camper = 'ficha_pago.html' #Nombre del template que se usa el html 

    template = template_env.get_template(html_info_camper)
 
    html_content = template.render(context) #Renderiza los datos en el html

    print("//////////")
    print(html_content)

    #Try para verificar paquete de libreria que permite usar la generacion de html a pdf 
    try:
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        output_pdf = "media/baucher_letter.pdf" #Nombre y ubicacion del archivo ya en pdf
        pdfkit.from_string(
            html_content, 
            output_pdf, 
            configuration=config,
            options = {
                'page-size': 'Letter',
                'margin-top': '0.25in',
                'margin-right': '0.25in',
                'margin-bottom': '0.25in',
                'margin-left': '0.25in',
                'encoding': "UTF-8"
                }
            )
         
    except OSError:
    #not present in PATH
        print("path_not_found")

    return output_pdf
    # config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')

