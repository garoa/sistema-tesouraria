# -*- coding: utf-8
#!/usr/bin/env python

import os
import sys
import django
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_tesouraria.settings")
django.setup()

from django.contrib.auth.models import User
from geral.models import Lancamento

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

# Cron roda dia 02, todo mes
@sched.scheduled_job('cron', day=2)
def faz_lancamentos():

    users = User.objects.all()
    descricao = 'Lançamento mensalidade mês %s-%s' % (timezone.now().month, timezone.now().year)

    for user in users:
        last_plano = user.associado.get_last_plano()
        if user.associado.is_in_anuidade():
            # Anuidade: Jah foi lancado
            continue
        elif user.associado.is_in_starving_hacker():
            # Starving: Lanca zero
            valor=0.0
        elif last_plano:
            # Mensal: Lanca 130
            valor = last_plano.valor
        else:
            # Sem Plano: Lanca 130
            valor = 130

        Lancamento.objects.create(
            user=user,
            autor='s',
            credito_debito='d',
            timestamp_comprovante=timezone.now(),
            valor=valor,
            descricao=descricao)

sched.start()
