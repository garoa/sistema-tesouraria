# -*- coding: utf-8

import sendgrid
import os
from sendgrid.helpers.mail import *

def sendgrid_cadastro(email_confirmation):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("tesZureirZ@garZa.net.br".replace('Z', 'o'))
    subject = "GAROA HC: Confirme sua conta."
    to_email = Email(email_confirmation.user.email)

    content = Content("text/plain", "Saudações pluviosa! Uma conta no sistema da tesouraria foi criada com este endereço de email. Se foi você mesmo que criou, por favor acesse o link de confirmação. Acesse: https://sistema-tesouraria.herokuapp.com/signup/confirmation/%s/" % (email_confirmation.hash_code))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)


def sendgrid_admin_libere():
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("nZreply-tesZuraria@garZa.net.br".replace('Z', 'o'))
    subject = "GAROA HC ADMIN: Libere o usuário."
    to_email = Email("tesZureirZ@garZa.net.br".replace('Z', 'o'))

    content = Content("text/plain", "Libere os usuários. Acesse: https://sistema-tesouraria.herokuapp.com/conselho/")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

def sendgrid_passwd_reset():
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("nZreply-tesZuraria@garZa.net.br".replace('Z', 'o'))
    subject = "GAROA HC ADMIN: Libere o usuário."
    to_email = Email("tesZureirZ@garZa.net.br".replace('Z', 'o'))

    content = Content("text/plain", "Libere os usuários. Acesse: https://sistema-tesouraria.herokuapp.com/conselho/")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

