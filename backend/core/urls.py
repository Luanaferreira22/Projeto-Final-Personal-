from django.urls import path, include
from . import views
from .views_aluno import login_aluno, logout_aluno, painel_aluno, alterar_senha_aluno

urlpatterns = [
    # Personal trainer
    path('',                      views.dashboard,           name='dashboard'),
    path('login/',                views.login_view,          name='login'),
    path('logout/',               views.logout_view,         name='logout'),
    path('politica-privacidade/', views.politica_privacidade,name='politica_privacidade'),

    # Aluno
    path('aluno/login/',          login_aluno,               name='login_aluno'),
    path('aluno/logout/',         logout_aluno,              name='logout_aluno'),
    path('aluno/painel/',         painel_aluno,              name='painel_aluno'),
    path('aluno/alterar-senha/',  alterar_senha_aluno,       name='alterar_senha_aluno'),

    # Agenda
    path('agenda/',               include('agenda.urls')),
]
