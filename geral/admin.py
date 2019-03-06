from django.contrib import admin
from geral.models import Associado
from geral.models import Lancamento
from geral.models import Plano

class PlanoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plano', 'descricao', 'validade_data_inicio',
            'data_validade_fim', 'approved_timestamp', 'moderation_status',
            'created_on')
    list_filter = ('moderation_status', 'user')
    search_fields = ('descricao',)


class LancamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'autor', 'credito_debito', 'valor', 'saldo',
            'descricao', 'approved_timestamp', 'moderation_status', 'created_on')
    list_filter = ('credito_debito', 'moderation_status', 'user')
    search_fields = ('descricao',)

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('saldo',)


# Register your models here.
admin.site.register(Associado)
admin.site.register(Plano, PlanoAdmin)
admin.site.register(Lancamento, LancamentoAdmin)
