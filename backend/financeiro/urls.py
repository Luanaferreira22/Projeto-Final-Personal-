from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pagamentos, name='lista_pagamentos'),
    path('registrar/', views.registrar_pagamento, name='registrar_pagamento'),
    path('<int:pk>/pagar/', views.marcar_pago, name='marcar_pago'),
    path('planos/', views.lista_planos, name='lista_planos'),
    path('planos/criar/', views.criar_plano, name='criar_plano'),
    path('planos/<int:pk>/editar/', views.editar_plano, name='editar_plano'),
    path('plano-valor/<int:pk>/', views.plano_valor, name='plano_valor'),
]
