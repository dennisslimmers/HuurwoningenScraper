import sys, os
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.parser import Parser

def send_mail(results, config):
    """Sends email with most recent search results"""

    gmail_user = config.sender  
    gmail_password = config.smtp_pw
    body = MIMEText(''.join(create_mail_body(results)).encode('utf-8').strip(), "html")

    msg = MIMEMultipart("alternative")
    msg["From"] = gmail_user  
    msg["To"] = config.reciever
    msg["Subject"] = 'HuurwoningenScraper found new hiring oppertunities for you!'  
    msg.attach(body)

    try:  
        server = smtplib.SMTP_SSL(config.smtp_server, int(config.port))
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.close()

        # Email successfully send, print a notification
        print("HWWS > New hiring oppertunities found! An email was send to: " + msg["To"])
    except:  
        e = sys.exc_info()[1]
        print(e)
        exit()


def create_mail_body(results):
    tableheader = open("./Templates/mail.tableheader.html", "r")
    tablefooter = open("./Templates/mail.tablefooter.html", "r")
    searchresults = ""

    for i in range (0, len(results)):
        result = results[i]
        
        template = open("./Templates/mail.searchresult.html", "r")
        searchresults += template.read() % (result.location, result.street, result.dwelling, result.rent, result.subtitle, result.description)

    return tableheader.read() + searchresults +  tablefooter.read()
        