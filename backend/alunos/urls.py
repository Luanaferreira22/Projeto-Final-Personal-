from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_alunos, name='lista_alunos'),
    path('cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('<int:pk>/', views.detalhe_aluno, name='detalhe_aluno'),
    path('<int:pk>/editar/', views.editar_aluno, name='editar_aluno'),
    path('<int:pk>/inativar/', views.inativar_aluno, name='inativar_aluno'),
    path('<int:pk>/excluir/', views.excluir_aluno, name='excluir_aluno'),
    path('<int:pk>/evolucao/', views.adicionar_evolucao, name='adicionar_evolucao'),
]