from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_treinos, name='lista_treinos'),
    path('criar/', views.criar_treino, name='criar_treino'),
    path('<int:pk>/', views.detalhe_treino, name='detalhe_treino'),
    path('<int:pk>/adicionar-exercicio/', views.adicionar_exercicio_treino, name='adicionar_exercicio_treino'),
    path('<int:pk>/remover-exercicio/<int:ex_pk>/', views.remover_exercicio_treino, name='remover_exercicio_treino'),
    path('exercicios/', views.lista_exercicios, name='lista_exercicios'),
    path('exercicios/criar/', views.criar_exercicio, name='criar_exercicio'),
]
