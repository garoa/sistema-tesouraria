# -*- coding: utf-8

from django.conf.urls import url
from geral import views
from django.views.generic import TemplateView

urlpatterns = (
    url(r'^$', TemplateView.as_view(template_name="geral/index.html"), name='index'),
    url(r'accounts/register/$', views.ContadorCreateView.as_view(), name='user-create'),
    url(r'minha-conta$', views.LancamentoListView.as_view(), name='lancamento-list'),
    url(r'submeter-comprovante$', views.LancamentoCreateView.as_view(), name='lancamento-create'),
    url(r'meus-planos$', views.PlanoListView.as_view(), name='plano-list'),
    url(r'incluir-planos$', views.PlanoCreateView.as_view(), name='plano-create'),
)
