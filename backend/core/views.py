from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from alunos.models import Aluno
from treinos.models import Treino
from financeiro.models import Pagamento, Plano
from datetime import date
import json


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            messages.error(request, 'Preencha o usuário e a senha.')
            return render(request, 'core/login.html')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request.GET.get('next', 'dashboard'))
            else:
                messages.error(request, 'Sua conta está inativa.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def politica_privacidade(request):
    return render(request, 'core/politica_privacidade.html')


@login_required
def dashboard(request):
    hoje = date.today()
    planos        = Plano.objects.filter(ativo=True)
    planos_labels = [p.nome for p in planos]
    planos_data   = [Pagamento.objects.filter(plano=p, pago=False).count() for p in planos]
    return render(request, 'core/dashboard.html', {
        'total_alunos':         Aluno.objects.filter(ativo=True).count(),
        'total_treinos':        Treino.objects.filter(ativo=True).count(),
        'total_planos':         Plano.objects.filter(ativo=True).count(),
        'pagamentos_pendentes': Pagamento.objects.filter(data_vencimento__lt=hoje, pago=False).count(),
        'alunos_recentes':      Aluno.objects.filter(ativo=True).order_by('-criado_em')[:5],
        'pagamentos_proximos':  Pagamento.objects.filter(pago=False, data_vencimento__gte=hoje).select_related('aluno','plano').order_by('data_vencimento')[:5],
        'planos_labels':        json.dumps(planos_labels),
        'planos_data':          json.dumps(planos_data),
    })
