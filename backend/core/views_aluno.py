from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from alunos.models import Aluno


def login_aluno(request):
    if request.method == 'POST':
        email       = request.POST.get('email', '').strip().lower()
        password    = request.POST.get('password', '')
        aceita_lgpd = request.POST.get('aceita_lgpd')

        if not email or not password:
            messages.error(request, 'Preencha e-mail e senha.')
            return render(request, 'core/login_aluno.html')

        if not aceita_lgpd:
            messages.error(request, 'Voce precisa aceitar os termos da LGPD para continuar.')
            return render(request, 'core/login_aluno.html')

        try:
            aluno = Aluno.objects.get(email=email, ativo=True)
        except Aluno.DoesNotExist:
            messages.error(request, 'E-mail ou senha invalidos.')
            return render(request, 'core/login_aluno.html')

        if not aluno.usuario:
            messages.error(request, 'Acesso nao configurado. Fale com seu personal trainer.')
            return render(request, 'core/login_aluno.html')

        user = authenticate(request, username=aluno.usuario.username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            # Salva aceite LGPD no banco
            aluno.aceite_lgpd      = True
            aluno.data_aceite_lgpd = timezone.now()
            aluno.save()
            return redirect('painel_aluno')
        else:
            messages.error(request, 'E-mail ou senha invalidos.')

    return render(request, 'core/login_aluno.html')


def logout_aluno(request):
    logout(request)
    return redirect('login_aluno')


def painel_aluno(request):
    if not request.user.is_authenticated:
        return redirect('login_aluno')

    if request.user.is_staff:
        return redirect('dashboard')

    try:
        aluno = Aluno.objects.get(usuario=request.user, ativo=True)
    except Aluno.DoesNotExist:
        logout(request)
        return redirect('login_aluno')

    from datetime import date
    from agenda.models import Aula
    hoje  = date.today()
    aulas = Aula.objects.filter(aluno=aluno, data__gte=hoje).order_by('data', 'hora_inicio')
    aulas_passadas = Aula.objects.filter(aluno=aluno, data__lt=hoje).order_by('-data')[:5]

    return render(request, 'agenda/agenda_aluno.html', {
        'aluno':          aluno,
        'aulas':          aulas,
        'aulas_passadas': aulas_passadas,
        'hoje':           hoje,
    })


def alterar_senha_aluno(request):
    """Permite o aluno trocar a própria senha"""
    if not request.user.is_authenticated:
        return redirect('login_aluno')

    if request.user.is_staff:
        return redirect('dashboard')

    if request.method == 'POST':
        senha_atual     = request.POST.get('senha_atual', '')
        nova_senha      = request.POST.get('nova_senha', '')
        confirmar_senha = request.POST.get('confirmar_senha', '')

        # Validacoes
        if not request.user.check_password(senha_atual):
            messages.error(request, 'Senha atual incorreta.')
            return render(request, 'core/alterar_senha_aluno.html')

        if len(nova_senha) < 6:
            messages.error(request, 'A nova senha deve ter pelo menos 6 caracteres.')
            return render(request, 'core/alterar_senha_aluno.html')

        if nova_senha != confirmar_senha:
            messages.error(request, 'A nova senha e a confirmacao nao conferem.')
            return render(request, 'core/alterar_senha_aluno.html')

        if senha_atual == nova_senha:
            messages.error(request, 'A nova senha deve ser diferente da senha atual.')
            return render(request, 'core/alterar_senha_aluno.html')

        # Salva a nova senha
        request.user.set_password(nova_senha)
        request.user.save()

        # Mantém o usuário logado após trocar a senha
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Senha alterada com sucesso!')
        return redirect('painel_aluno')

    return render(request, 'core/alterar_senha_aluno.html')
