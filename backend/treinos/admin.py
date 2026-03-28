from django.contrib import admin
from .models import Exercicio, Treino, TreinoExercicio

@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'grupo_muscular']
    list_filter = ['grupo_muscular']
    search_fields = ['nome']

@admin.register(Treino)
class TreinoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'aluno', 'ativo', 'criado_em']
    list_filter = ['ativo']
    search_fields = ['nome', 'aluno__nome']

admin.site.register(TreinoExercicio)
