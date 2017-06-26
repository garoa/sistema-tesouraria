# -*- coding: utf-8

from django.conf.urls import url
from geral import views
from django.views.generic import TemplateView

urlpatterns = (
    url(r'^$', TemplateView.as_view(template_name="geral/index.html")),
    url(r'minha-conta$', views.LancamentoListView.as_view(), name='lancamento-list'),
)
