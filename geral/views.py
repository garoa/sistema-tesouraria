# -*- coding: utf-8

import json
import requests

from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import CreateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView

from geral.models import Plano
from geral.models import Lancamento
from geral.form import UserForm
from geral.form import PasswordResetFormSendgrid


class PlanoListView(LoginRequiredMixin, ListView):

    model = Plano

    def get_queryset(self):
        return Plano.objects.filter(
                user=self.request.user
                ).order_by('approved_timestamp', 'id')


class LancamentoListView(LoginRequiredMixin, ListView):

    model = Lancamento

    def get_queryset(self):
        return Lancamento.objects.filter(
                user=self.request.user
                ).order_by('approved_timestamp', 'id')


class LancamentoCreateView(LoginRequiredMixin, CreateView):
    fields = ['valor', 'timestamp_comprovante', 'comprovante', 'descricao']
    model = Lancamento

    def form_valid(self, form):
        lancamento = form.save(commit=False)
        lancamento.autor = 'u'
        lancamento.user = self.request.user
        lancamento.credito_debito = 'c'
        lancamento.comprovante = self.request.FILES['comprovante']

        return super(LancamentoCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lancamento-list')


class PlanoCreateView(LoginRequiredMixin, CreateView):
    fields = ['plano']
    model = Plano

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.autor = 'u'
        obj.user = self.request.user
        obj.valor = Plano.PLANO_PRICES[obj.plano]

        return super(PlanoCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('plano-list')



class ContadorCreateView(CreateView):
    model = User
    form_class = UserForm

    def form_valid(self, form):

        response = requests.post('https://www.google.com/recaptcha/api/siteverify',
                data = {'secret':'6LevmisUAAAAAAAn7YTyb0g7nQH60-J_9wDyAl0y',
                        'remoteip': self.request.META.get('REMOTE_ADDR', ''),
                        'response': self.request.POST.get('g-recaptcha-response', '')})

        response_payload = json.loads(response.text)

        if not response_payload['success']:
            return redirect('https://www.youtube.com/watch?v=QH2-TGUlwu4')

        if self.request.POST.get('honeypot', ''):
            return redirect('https://www.youtube.com/watch?v=KgbSjRMqyjc')

        return super(ContadorCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')

class PasswordResetViewSendgrid(PasswordResetView):
    form_class = PasswordResetFormSendgrid
