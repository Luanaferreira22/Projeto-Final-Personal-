from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Aluno, EvolutionFisica
from .forms import AlunoForm, EvolutionFisicaForm
import re
import secrets
import string


def _gerar_senha_temporaria():
    """Gera uma senha temporária segura de 10 caracteres"""
    caracteres = string.ascii_letters + string.digits + "!@#$"
    return ''.join(secrets.choice(caracteres) for _ in range(10))


def _criar_usuario_aluno(nome, email):
    """
    Cria o usuário Django para o aluno.
    Senha temporária gerada aleatoriamente — não é mais o email.
    """
    base = email.split('@')[0]
    base = re.sub(r'[^a-zA-Z0-9_]', '', base)
    username = base
    counter  = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1

    senha_temp = _gerar_senha_temporaria()

    user = User.objects.create_user(
        username=username,
        email=email,
        password=senha_temp,
        first_name=nome.split()[0],
        is_staff=False,
        is_superuser=False,
    )
    return user, senha_temp


@login_required
def lista_alunos(request):
    query  = request.GET.get('q', '')
    alunos = Aluno.objects.filter(ativo=True)
    if query:
        alunos = alunos.filter(nome__icontains=query)
    return render(request, 'alunos/lista.html', {'alunos': alunos, 'query': query})


@login_required
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            aluno = form.save(commit=False)
            email = form.cleaned_data['email']
            nome  = form.cleaned_data['nome']

            user, senha_temp = _criar_usuario_aluno(nome, email)
            aluno.usuario = user
            aluno.save()

            messages.success(
                request,
                f'Aluno {aluno.nome} cadastrado! '
                f'Login: {email} | Senha temporaria: {senha_temp} '
                f'(oriente o aluno a trocar no primeiro acesso)'
            )
            return redirect('lista_alunos')
        else:
            messages.error(request, 'Corrija os erros abaixo antes de salvar.')
    else:
        form = AlunoForm()
    return render(request, 'alunos/form.html', {'form': form, 'titulo': 'Cadastrar Aluno'})


@login_required
def editar_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            if aluno.usuario:
                aluno.usuario.email = form.cleaned_data['email']
                aluno.usuario.save()
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('lista_alunos')
        else:
            messages.error(request, 'Corrija os erros abaixo antes de salvar.')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'alunos/form.html', {
        'form': form, 'titulo': 'Editar Aluno', 'aluno': aluno
    })


@login_required
def detalhe_aluno(request, pk):
    aluno      = get_object_or_404(Aluno, pk=pk)
    evolucoes  = aluno.evolucoes.all()[:10]
    treinos    = aluno.treinos.all()
    pagamentos = aluno.pagamentos.all().order_by('-data_vencimento')[:5]
    from agenda.models import Aula
    from datetime import date
    proximas_aulas = Aula.objects.filter(aluno=aluno, data__gte=date.today()).order_by('data')[:5]
    return render(request, 'alunos/detalhe.html', {
        'aluno': aluno, 'evolucoes': evolucoes,
        'treinos': treinos, 'pagamentos': pagamentos,
        'proximas_aulas': proximas_aulas,
    })


@login_required
def inativar_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    aluno.ativo = False
    aluno.save()
    messages.success(request, f'Aluno {aluno.nome} inativado.')
    return redirect('lista_alunos')


@login_required
def adicionar_evolucao(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        form = EvolutionFisicaForm(request.POST)
        if form.is_valid():
            ev       = form.save(commit=False)
            ev.aluno = aluno
            ev.save()
            messages.success(request, 'Evolucao fisica registrada!')
            return redirect('detalhe_aluno', pk=pk)
    else:
        form = EvolutionFisicaForm()
    return render(request, 'alunos/evolucao_form.html', {'form': form, 'aluno': aluno})
