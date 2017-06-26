# -*- coding: utf-8

from django.views.generic.list import ListView
from django.views.generic import CreateView

from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

from geral.models import Plano
from geral.models import Lancamento


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

        return super(LancamentoCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lancamento-list')
