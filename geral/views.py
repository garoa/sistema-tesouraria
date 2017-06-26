# -*- coding: utf-8

from django.views.generic.list import ListView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from geral.models import Lancamento

class LancamentoListView(LoginRequiredMixin, ListView):

    model = Lancamento

    def get_queryset(self):
        return Lancamento.objects.filter(
                user=self.request.user
                ).order_by('approved_timestamp', 'id')
