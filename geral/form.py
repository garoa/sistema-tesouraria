import sendgrid
import os
from sendgrid.helpers.mail import *

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.template import loader

from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
import django.contrib.auth.password_validation as validators

class UserForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'date_joined', 'password']

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        required=False,
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        required=False,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        if password1:
            password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.is_active = False
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


class PasswordResetFormSendgrid(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        #email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        #if html_email_template_name is not None:
        #    html_email = loader.render_to_string(html_email_template_name, context)
        #    email_message.attach_alternative(html_email, 'text/html')

        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        subject = loader.render_to_string(subject_template_name, context)
        from_email = Email("tesZureirZ@garZa.net.br".replace('Z', 'o'))
        to_email = Email(to_email)
        body = Content("text/plain",
                loader.render_to_string(email_template_name, context))
        mail = Mail(from_email, subject, to_email, body)

        response = sg.client.mail.send.post(request_body=mail.get())

        print(response.status_code)
        print(response.body)
        print(response.headers)

