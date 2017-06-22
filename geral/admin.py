from django.contrib import admin
from geral.models import Associado
from geral.models import Lancamento
from geral.models import Plano

# Register your models here.
admin.site.register(Associado)
admin.site.register(Lancamento)
admin.site.register(Plano)
