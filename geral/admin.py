from django.contrib import admin
from geral.models import Associado
from geral.models import Lancamento
from geral.models import Plano

class LancamentoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'user', 'saldo', 'approved_timestamp', 'moderation_status')
    list_filter = ('user', 'credito_debito', 'moderation_status')
    search_fields = ('descricao',)

admin.site.register(Lancamento, LancamentoAdmin)

# Register your models here.
admin.site.register(Associado)
admin.site.register(Plano)
