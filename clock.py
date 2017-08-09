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

# Cron roda dia 01, todo mes
@sched.scheduled_job('cron', day=2)
def faz_lancamentos():
    users = User.objects.all()

    # TODO:
    # Verificar Starving Hacker
    # Verificar Anuidade
    # Verificar valor 85, 130

    descricao = 'Lançamento mensalidade mês %s-%s' % (timezone.now().month, timezone.now().year)

    for user in users:
        Lancamento.objects.create(
            user=user,
            autor='s',
            credito_debito='d',
            timestamp_comprovante=timezone.now(),
            valor=85.0,
            descricao=descricao)

sched.start()
