
from django.utils import timezone
from django.views.generic import RedirectView
from django.shortcuts import redirect
from django.http import Http404
from django.contrib.auth.models import User
from .models import EmailConfirmation

from .mail_shortcuts import sendgrid_admin_libere

class EmailConfirmationView(RedirectView):

    def get(self, request, *args, **kwargs):

        hash_code = kwargs.get('hash_code')
        if EmailConfirmation.objects.filter(
                hash_code=hash_code).count() == 1:
            cc = EmailConfirmation.objects.get(hash_code=hash_code)
            cc.confirmation_date = timezone.now()
            #cc.user.is_active = True
            cc.user.is_staff = False
            cc.user.save()
            cc.save()

            #Manda email para Admin
            sendgrid_admin_libere()
            return redirect('email-confirmed')

        else:
            raise Http404
