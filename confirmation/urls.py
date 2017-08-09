from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^confirmation/(?P<hash_code>\w+)/$', views.EmailConfirmationView.as_view(),
        name='email_confirmation'),
    url(r'^confirmation/email-confirmed/$', TemplateView.as_view(
        template_name='confirmation/email-confirmed.html'), name='email-confirmed'),
]
