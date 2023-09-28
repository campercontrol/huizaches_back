import requests

domain_name = "campercontrol.com"
mailgun_api_key = "key-de3828f749bc30729dad5eadf0620a24"
from_user_email = "dev@campercontrol.com"
to_user_email = "almazanmendez@hotmail.com"


def send_simple_message_test():
    return requests.post(
        f"https://api.mailgun.net/v3/{domain_name}/messages",
        auth=("api", mailgun_api_key),
        data={"from": from_user_email,
              "to": [to_user_email],
              "subject": "Welcome",
              "text": "Testing some Mailgun awesomness!"})

def send_simple_message(from_user:str,to_users:list,email_subject:str,text_message:str) -> dict:
    return requests.post(
        f"https://api.mailgun.net/v3/{domain_name}/messages",
        auth=("api", mailgun_api_key),
        data={"from": from_user_email,
              "to": to_users,
              "subject": email_subject,
              "text": text_message})
