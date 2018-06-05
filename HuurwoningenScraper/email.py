import sys, os
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.parser import Parser

def send_mail(result):
    """Sends email with most recent search results"""

    gmail_user = 'from@gmail.com'  
    gmail_password = 'test12345'
    body = MIMEText(create_mail_body(result), "plain")

    msg = MIMEMultipart("alternative")
    msg["From"] = gmail_user  
    msg["To"] = 'to@gmail.nl'
    msg["Subject"] = 'HuurwoningenScraper found a new hiring oppertunity for you!'  
    msg.attach(body)

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.close()

        # Email successfully send, print a notification
        print("New Hiring oppertunity found! An email was send to: " + msg["To"])
    except:  
        e = sys.exc_info()[0]
        print(e)
        exit()


def create_mail_body(result):
    return f"""\
Location: {result.location}
Street: {result.street}
Dwelling: {result.dwelling}
Rent: {result.rent}

{result.subtitle.strip()}

{result.description}
""" 
        