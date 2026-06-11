"""
Personal Manager — Middleware de Controle de Acesso
Bloqueia usuarios do tipo aluno (is_staff=False) de acessarem
as rotas administrativas do personal trainer.
"""
from django.shortcuts import redirect


class BloqueioAlunoMiddleware:
    """
    Alunos autenticados so podem acessar as rotas da area do aluno.
    Qualquer tentativa de acesso a rotas do personal (dashboard,
    alunos, treinos, financeiro, agenda) e redirecionada para o
    painel do aluno.
    """

    # Prefixos de URL permitidos para o aluno
    ROTAS_PERMITIDAS_ALUNO = (
        '/aluno/',
        '/login/',
        '/logout/',
        '/politica-privacidade/',
        '/static/',
        '/media/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated and not user.is_staff:
            permitido = any(
                request.path.startswith(rota)
                for rota in self.ROTAS_PERMITIDAS_ALUNO
            )
            if not permitido:
                return redirect('painel_aluno')

        return self.get_response(request)
