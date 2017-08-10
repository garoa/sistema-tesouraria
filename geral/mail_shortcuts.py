# -*- coding: utf-8

import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

def sendgrid_alert_admin():
    subject = "GAROA HC ADMIN: Existem Lançamentos e Planos pendentes"
    to_email = Email("tesZureirZ@garZa.net.br".replace('Z', 'o'))
    from_email = Email("nZreply-tesZuraria@garZa.net.br".replace('Z', 'o'))

    content = Content("text/plain", "Libere os lançamentos/planos dos usuários. Acesse: https://sistema-tesouraria.herokuapp.com/conselho/")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)


def sendgrid_lancamento(lancamento):
    subject = "GAROA HC: Um lançamento foi registrado na sua conta."
    to_email = Email(lancamento.user.email)
    from_email = Email("tesZureirZ@garZa.net.br".replace('Z', 'o'))

    content = Content("text/plain", "Um lançamento foi registrado na sua conta. Acesse: https://sistema-tesouraria.herokuapp.com/")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

