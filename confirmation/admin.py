from django.contrib import admin

# Register your models here.
from .models import EmailConfirmation
admin.site.register(EmailConfirmation)
