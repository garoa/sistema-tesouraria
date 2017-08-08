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


@sched.scheduled_job('cron', day=1)
def faz_lancamentos():
    users = User.objects.all()

    for user in users:
        Lancamento.objects.create(
            user=user,
            autor='s',
            credito_debito='d',
            timestamp_comprovante=timezone.now(),
            valor=85.0,
            descricao='Lançamento mensalidade mês %s' % timezone.now().month,
        )

sched.start()
