"""
Personal Manager — Decorators de Seguranca
Bloqueia alunos de acessarem rotas administrativas do personal trainer.

Uso:
    from core.decorators import personal_required

    @personal_required
    def minha_view(request):
        ...
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def personal_required(view_func):
    """
    Garante que apenas o personal trainer (is_staff=True) acesse a rota.
    Alunos autenticados (is_staff=False) sao redirecionados para o painel deles.
    Usuarios nao autenticados vao para o login.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, 'Acesso restrito ao personal trainer.')
            return redirect('painel_aluno')
        return view_func(request, *args, **kwargs)
    return wrapper
