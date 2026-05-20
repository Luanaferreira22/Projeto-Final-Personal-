from django.contrib import admin
from .models import Aluno, EvolutionFisica

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'ativo', 'criado_em']
    list_filter = ['ativo', 'sexo']
    search_fields = ['nome', 'email']

@admin.register(EvolutionFisica)
class EvolutionFisicaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'data', 'peso', 'altura', 'imc']
    list_filter = ['data']