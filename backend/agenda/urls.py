from django.urls import path
from . import views

urlpatterns = [
    path('',              views.agenda_personal, name='agenda_personal'),
    path('agendar/',      views.agendar_aula,    name='agendar_aula'),
    path('editar/<int:pk>/', views.editar_aula,  name='editar_aula'),
    path('cancelar/<int:pk>/', views.cancelar_aula, name='cancelar_aula'),
]
