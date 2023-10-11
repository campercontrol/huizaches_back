import requests
import json

toku_base_url = "https://api.trytoku.com"
TOKU_API_KEY = ""
ACCOUNT_KEY = "" #Difiere dependiendo la cuenta que se necesite usar

"""
    ## Toku Payments Consideraciones
    ### -- Autentificacion --
    ### API-key: 
        - La API Key es el identificador único de tu Organización 
        - Toku autentica tus llamadas a la API mediante API Keys. 
          En cada una de las llamadas hacia la API de Toku, debes incluir tu API Key en el campo x-api-key del Header.
        - La Account Key es el identificador único de cada Cuenta de Cobro
        - Ciertos objetos permiten ser asociados a Cuentas de Cobro especificas. En cada una de las llamadas hacia la API de Toku, 
          opcionalmente puedes incluir una Account Key en el campo x-account-key del Header.
        - El header x-account-key es opcional. Solo debes considerarlo si configuraste más de una Cuenta de Cobro. 
          Si no se incluye, se considera la Cuenta de Cobro predeterminada.
"""
 
def test_request():
    headers = {
        'Content-Type' : 'application/json',
        'Accept' : 'application/json',
        'x-api-key' : f'{TOKU_API_KEY}',
        'x-account-key' : f'{ACCOUNT_KEY}'
    }

    return requests.post(
        headers=headers,
        data={
            "id": "cus_lq1wGjwgFyqQm4ACZx0QjE84qKm8fffa",
            "mail": "jon@snow.got",
            "name": "Jon Snow",
            "phone_number": "+56987654321"    
            }
        )


#<-----------------Customer------------------>


def create_customer(user_id:str,email:str,name:str,phone:str,send_email:bool):
    """
    id	                            string	            Identificador único del Customer.	

    *external_id 	                string	            Identificador único del Customer 
                                                        definido por la Organización. (Campo requerido)	

    *government_id	                string	            Identificador personal del Customer 
                                                        según su nacionalidad.	(Campo requerido)

    *mail	                        string	            Correo que se utilizará para contactar al Customer.	(Campo requerido)

    name	                        string	            Nombre por el cual nos referimos al Customer en los 
                                                        mensajes.	

    phone_number	                string	            Número de teléfono del Customer para contactarlo por 
                                                        SMS y Whatsapp.	

    pac_mandate_id	                string	            Identificador del mandato que se pondrá al inscribir el 
                                                        PAC asociado al Customer	

    default_agent	                string	            Correo del agente que tendrá asignado por defecto el Customer 
                                                        en caso de que este responda alguno de los mensajes enviados a 
                                                        través de la plataforma.	

    send_mail	                    boolean	            Flag que nos indica si quieres iniciar el envío automático 
                                                        de recordatorios de inscripción de medio de pago al crear el customer. 
                                                        Se le enviará con la secuencia "Mensajes automáticos para registro de 
                                                        medios de pago"	

    agent_phone_number	            string	            Teléfono del agente asignado	

    silenced_until	                date-time           Fecha hasta la cual será silenciado el Customer. 
                                                        No recibirá mensajes hasta después de la fecha seleccionada.	

    metadata	                    json	            Valores adicionales específicos de cada Customer. 
                                                        Son tratados como valores de texto y que no pueden tener más de 256 caracteres cada uno. 
                                                        Debes agregarlos en la webapp de Toku antes de poder utilizarlos aquí.	

    secondary_emails	            array	            Lista de los emails secundarios a los que se va a reenviar 
                                                        la mensajería que se envíe al customer.	(Activable debe pedirse a toku)

    default_receipt_type            string	            Tipo de recibo a emitir por defecto para este Customer. 
                                                        Puede tomar los valores bill o invoice para hacer referencia a 
                                                        facturas o boletas respectivamente.	(Requerido para modulo de facturacion)

    rfc     	                    string              Registro Federal de Contribuyentes de México.	(Requerido para modulo de facturacion / Solo utilizado para mexico)

    tax_zip_code  	                string	            Codigo postal del domicilio para México.	(Requerido para modulo de facturacion / Solo utilizado para mexico)

    fiscal_regime 	                string	            Regimen fiscal del Customer.	(Requerido para modulo de facturacion / Solo utilizado para mexico)
    """

    url_customer = f"{toku_base_url}/customers"
    headers = {
        'Content-Type' : 'application/json',
        'Accept' : 'application/json',
        'x-api-key' : f'{TOKU_API_KEY}',
        # 'x-account-key' : f'{ACCOUNT_KEY}'
    }
    payload = {
        "send_mail": send_email,
        "government_id": user_id,  #Curp (MX) RUT(CHL) 
        "external_id": user_id, #usar uuid
        "mail": email,
        "name": name,
        "phone_number": phone#"+56987654321"
    }

    print(payload)

    response = requests.post(url_customer, json=payload, headers=headers)
    return response

    
def get_customer(customer_id):
    url_customer = f"{toku_base_url}/customers/{customer_id}"

    headers = {
        "accept": "application/json",
        'x-api-key' : f'{TOKU_API_KEY}',
        }

    response = requests.get(url_customer, headers=headers)

    return response


#<-----------------Invoice------------------>


def create_invoice(customer_id:str,product_id:str,due_date:str,amount:str):

    url = f"{toku_base_url}/invoices"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'x-api-key' : f'{TOKU_API_KEY}',
    }

    payload = {
        "is_paid": False,
        "is_void": False,
        "disable_automatic_payment": False,
        "customer": customer_id,
        "product_id": product_id,
        "due_date": due_date,
        "amount": amount
    }

    response = requests.post(url, json=payload, headers=headers)
    # print(response.text)
    return response


def get_invoice(invoice_id):
    url = f"{toku_base_url}/invoices/{invoice_id}"

    headers = {
        "accept": "application/json",
        'x-api-key' : f'{TOKU_API_KEY}',
        }

    response = requests.get(url, headers=headers)


def delete_invoice(invoice_id):
    url = f"{toku_base_url}/invoices/{invoice_id}/void"

    payload = { "delete_invoice": False }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'x-api-key' : f'{TOKU_API_KEY}',
    }

    response = requests.post(url, json=payload, headers=headers)


def get_invoice_by_customer(customer_id):
    url = f"{toku_base_url}/invoices/customer/{customer_id}"
    headers = {
        "accept": "application/json",
        'x-api-key' : f'{TOKU_API_KEY}',
        }

    response = requests.get(url, headers=headers)


#<-----------------Subscripcion------------------>


def create_subscription():

    url = f"{toku_base_url}/subscriptions"

    payload = {
        "is_recurring": False,
        "customer": "cus_M2aYvh3QOfVylcre5gIMyIhYPrHBKfw2",
        "product_id": "92792"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'x-api-key' : f'{TOKU_API_KEY}',
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def update_suscription():
    url = f"{toku_base_url}/subscriptions"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'x-api-key' : f'{TOKU_API_KEY}',
    }
    payload = {
        "is_recurring": False,
        "customer": " ",
        "product_id": " "
    }

    response = requests.put(url, json=payload, headers=headers)

    print(response.text)


def get_subscription(subscription_id):
    url = f"{toku_base_url}/subscriptions/{subscription_id}"

    headers = {
        "accept": "application/json",
        'x-api-key' : f'{TOKU_API_KEY}',
        }

    response = requests.get(url, headers=headers)

    print(response.text)


def delete_subscription(subscription_id):
    url = f"{toku_base_url}/subscriptions/{subscription_id}"

    headers = {
        "accept": "application/json",
        'x-api-key' : f'{TOKU_API_KEY}',
        }

    response = requests.delete(url, headers=headers)

    print(response.text)


def get_subscription_by_customer(customer_id):
    url = f"{toku_base_url}/subscriptions/customer/{customer_id}"

    headers = {
        "accept": "application/json",
        'x-api-key' : f'{TOKU_API_KEY}',
        }

    response = requests.get(url, headers=headers)

    print(response.text)


#<-----------------Webhook------------------>

enabled_events = [
    "interaction.incoming",#Interaction entrante desde un Customer hacia Toku.
    "interaction.outgoing",#Interaction saliente desde Toku hacia un Customer.
    "payment_method.attached",#Customer ha inscrito un método de pago en la plataforma.
    "payment_method.attached_products",#Customer ha inscrito un método de pago en la plataforma y envía una lista de los productos asociados. (Recomendado para organizaciones en modo suscription)
    "payment_method_inscription_intent.failed",#Intento de inscripción de un método de pago fallido
    "payment_intent.succeeded",#Intento de pago exitoso de un Invoice.
    "payment_intent.payment_failed",# Intento de pago fallido de un Invoice.
    "payment_intent.succeeded_batch",#Resumen de pagos exitosos para una lista de Invoices. Se utiliza en procesos de cobro automático masivos
    "payment_intent.payment_failed_batch",#Resumen de intentos de pagos fallidos para una lista de Invoices. Se utiliza en procesos de cobro automático masivos
    "payment_intent.payment_pending_batch",#Resumen de intentos de pagos que se encuentran pendientes para una lista de Invoices. Se utiliza en procesos de cobro automático masivos
    "payment.succeeded",#Pago realizado exitosamente de un Invoice. Esto aplica solo para pagos ejecutados manualmente a través de Toku. Si quieres escuchar los pagos procesados a través de Toku, debes utilizar payment_intent.succeeded.
    "activation.created",#Creación y actualización de una activación de transferencia. Esto se realiza mediante el proceso de la transferencia de $1.000 CLP por parte de un customer y el webhook se gatilla tanto en el minuto que se realiza la transferencia, como también cuando el customer queda activo.
    "bank_account_verification.result",#Respuesta de la validación de una cuenta CLABE. Notifica la información que se obtuvo producto de una validación. 
    "payout.done",#Actualización de las liquidaciones efectuadas por parte de Toku hacia la organización. Entrega información sobre los pagos, la conciliación de estos y sus Invoices
    ]

status_webhook_toku = [
    "enabled",#Activo 
    "disable",#Inactivo
]

def create_webhook_toku(enabled_events,status,url_webhook):

    url = f"{toku_base_url}/webhook_endpoints"

    # payload = {
    #     "enabled_events": ["payment_method.attached", "payment_intent.succeeded"],
    #     "status": "enabled",
    #     "url": "https://prueba.com"
    # }
    payload = {
        "enabled_events": enabled_events,
        "status": status,
        "url": url_webhook
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'x-api-key' : f'{TOKU_API_KEY}',
    }

    response = requests.post(url, json=payload, headers=headers)

    return response


def get_webhooks_toku():
    url = f"{toku_base_url}/webhook_endpoints"

    headers = {
        "accept": "application/json",
        "x-api-key": f"{TOKU_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    return response


def get_webhooks_by_id_toku(id):

    url = f"{toku_base_url}/webhook_endpoints/{id}"

    headers = {
        "accept": "application/json",
        "x-api-key": f"{TOKU_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    return response


def update_webhooks_toku(id):
    url = f"{toku_base_url}/webhook_endpoints/{id}"

    payload = {
        "enabled_events": ["payment_method.attached", "payment_method.attached"],
        "url": "https://prueba.com",
        "status": "enabled"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": f"{TOKU_API_KEY}"
    }

    response = requests.put(url, json=payload, headers=headers)

    return response


def test_webhook_tou():
    url = f"{toku_base_url}/dummy_webhook"

    payload = {
        "event_type": "interaction.incoming",
        "url": "https://prueba.com"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": f"{TOKU_API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response


#<-----------------Sequences------------------>
#Promocion de campañas 


#<-----------------Redirection------------------>

def create_redirection_toku():
    url = f"{toku_base_url}/redirection"

    payload = {
        "success_url": "https://example.com/success",
        "failure_url": "https://example.com/failure"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": f"{TOKU_API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def update_redirection_toku():
    url = f"{toku_base_url}/redirection"

    payload = {
        "success_url": "None",
        "failure_url": "None",
        "id": "red_6D1vT6JHh84oKdi9xgvAhcNcsKDerv6J"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": f"{TOKU_API_KEY}"
    }

    response = requests.put(url, json=payload, headers=headers)

    print(response.text)


#<-----------------Redirection------------------>


#<-----------------Payments------------------>

def get_payments(page,page_size,start_date,end_date):

    url = f"{toku_base_url}/organization/payments?page={page}&page_size={page_size}&start_date={start_date}&end_date={end_date}"

    headers = {
        "accept": "application/json",
        "x-api-key": f"{TOKU_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    return response 