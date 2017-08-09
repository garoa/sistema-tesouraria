from django.db import models

from django.db.models.signals import post_save
from django.contrib.auth.models import User

import random
from .mail_shortcuts import sendgrid_cadastro

class EmailConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash_code = models.CharField(max_length=100, default='')
    confirmation_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

def create_hash(sender, instance, created, **kwargs):

    if kwargs.get('raw', False):
        # https://code.djangoproject.com/ticket/17880
        return

    if created:
        hash_code = ''.join(random.choice('0123456789ABCDEF') for i in range(25))
        email_confirmation = EmailConfirmation.objects.create(user=instance, hash_code=hash_code)
        mail_shortcuts(email_confirmation)
        print("Confirmacao email enviado.")

post_save.connect(create_hash, sender=User)

