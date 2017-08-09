# -*- coding: utf-8

import sendgrid
import os
from sendgrid.helpers.mail import *

def sendgrid_cadastro(lancamento):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("tesZureirZ@garZa.net.br".replace('Z', 'o'))
    subject = "GAROA HC: Confirme sua conta."
    to_email = Email(lancamento.user.email)

    content = Content("text/plain", "Um lançamento foi registrado na sua conta. Acesse: https://sistema-tesouraria.herokuapp.com/")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)


def sendgrid_lancamento(lancamento):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("tesZureirZ@garZa.net.br".replace('Z', 'o'))
    subject = "GAROA HC: Um lançamento foi registrado na sua conta."
    to_email = Email(lancamento.user.email)
    content = Content("text/plain", "Um lançamento foi registrado na sua conta. Acesse: https://sistema-tesouraria.herokuapp.com/")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

