from django.contrib import admin
from geral.models import Associado
from geral.models import Lancamento
from geral.models import Plano

class PlanoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plano', 'descricao', 'data_validade_fim', 'data_validade_fim', 'approved_timestamp', 'moderation_status',)
    list_filter = ('moderation_status', 'user')
    search_fields = ('descricao',)


class LancamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'autor', 'credito_debito', 'valor', 'saldo', 'descricao', 'approved_timestamp', 'moderation_status',)
    list_filter = ('credito_debito', 'moderation_status', 'user')
    search_fields = ('descricao',)


# Register your models here.
admin.site.register(Associado)
admin.site.register(Plano, PlanoAdmin)
admin.site.register(Lancamento, LancamentoAdmin)
