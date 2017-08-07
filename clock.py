#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_tesouraria.settings")
django.setup()

from geral.models import Lancamento

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

# Cron roda dia 01, todo mes
@sched.scheduled_job('cron', day=1)
def faz_lancamentos():
    # TODO
    print('faz_lancamentos')

sched.start()
