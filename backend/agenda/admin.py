from django.contrib import admin
from .models import Aula

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display  = ['aluno', 'data', 'hora_inicio', 'hora_fim', 'situacao']
    list_filter   = ['situacao', 'data']
    search_fields = ['aluno__nome']
