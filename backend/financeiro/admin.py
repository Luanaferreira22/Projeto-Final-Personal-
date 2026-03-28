from django.contrib import admin
from .models import Plano, Pagamento

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'valor', 'duracao', 'ativo']

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'plano', 'valor', 'data_vencimento', 'pago']
    list_filter = ['pago', 'plano']
    search_fields = ['aluno__nome']
