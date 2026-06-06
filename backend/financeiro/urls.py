from django.urls import path
from . import views

urlpatterns = [
    # Pagamentos
    path('',                        views.lista_pagamentos,   name='lista_pagamentos'),
    path('registrar/',              views.registrar_pagamento,name='registrar_pagamento'),
    path('<int:pk>/editar/',        views.editar_pagamento,   name='editar_pagamento'),
    path('<int:pk>/pago/',          views.marcar_pago,        name='marcar_pago'),
    # Planos
    path('planos/',                 views.lista_planos,       name='lista_planos'),
    path('planos/criar/',           views.criar_plano,        name='criar_plano'),
    path('planos/<int:pk>/editar/', views.editar_plano,       name='editar_plano'),
    path('planos/valor/<int:pk>/',  views.plano_valor,        name='plano_valor'),
    # Plano do aluno
    path('plano-aluno/<int:aluno_pk>/', views.plano_aluno,   name='plano_aluno'),
]
