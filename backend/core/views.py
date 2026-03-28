from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from alunos.models import Aluno, EvolutionFisica
from treinos.models import Treino
from financeiro.models import Pagamento, Plano
from django.utils import timezone
from datetime import date


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    total_alunos = Aluno.objects.filter(ativo=True).count()
    total_treinos = Treino.objects.count()
    total_planos = Plano.objects.count()

    hoje = date.today()
    pagamentos_pendentes = Pagamento.objects.filter(
        data_vencimento__lt=hoje,
        pago=False
    ).count()

    alunos_recentes = Aluno.objects.filter(ativo=True).order_by('-criado_em')[:5]

    pagamentos_proximos = Pagamento.objects.filter(
        pago=False,
        data_vencimento__gte=hoje
    ).order_by('data_vencimento')[:5]

    # Dados para grafico de alunos por plano
    planos = Plano.objects.all()
    planos_labels = [p.nome for p in planos]
    planos_data = [Pagamento.objects.filter(plano=p, pago=False).count() for p in planos]

    context = {
        'total_alunos': total_alunos,
        'total_treinos': total_treinos,
        'total_planos': total_planos,
        'pagamentos_pendentes': pagamentos_pendentes,
        'alunos_recentes': alunos_recentes,
        'pagamentos_proximos': pagamentos_proximos,
        'planos_labels': planos_labels,
        'planos_data': planos_data,
    }
    return render(request, 'core/dashboard.html', context)
