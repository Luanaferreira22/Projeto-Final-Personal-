from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Aluno, EvolutionFisica
from .forms import AlunoForm, EvolutionFisicaForm


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
            # commit=False segura o save para associar o usuário antes de gravar
            aluno = form.save(commit=False)
            email = form.cleaned_data['email']

            # garante username único caso dois alunos tenham o mesmo prefixo de email
            username      = email.split('@')[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user = User.objects.create_user(
                username=username, email=email, password='aluno@123',
                first_name=form.cleaned_data['nome'].split()[0],
            )
            aluno.usuario = user
            aluno.save()
            messages.success(request, f'Aluno {aluno.nome} cadastrado com sucesso!')
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
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('lista_alunos')
        else:
            messages.error(request, 'Corrija os erros abaixo antes de salvar.')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'alunos/form.html', {'form': form, 'titulo': 'Editar Aluno', 'aluno': aluno})


@login_required
def detalhe_aluno(request, pk):
    aluno      = get_object_or_404(Aluno, pk=pk)
    evolucoes  = aluno.evolucoes.all()[:10]
    treinos    = aluno.treinos.all()
    pagamentos = aluno.pagamentos.all().order_by('-data_vencimento')[:5]
    return render(request, 'alunos/detalhe.html', {
        'aluno': aluno, 'evolucoes': evolucoes,
        'treinos': treinos, 'pagamentos': pagamentos,
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
            evolucao       = form.save(commit=False)
            evolucao.aluno = aluno
            evolucao.save()
            messages.success(request, 'Evolução física registrada com sucesso!')
            return redirect('detalhe_aluno', pk=pk)
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = EvolutionFisicaForm()
    return render(request, 'alunos/evolucao_form.html', {'form': form, 'aluno': aluno})
@login_required
def excluir_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        nome = aluno.nome
        aluno.delete()
        messages.success(request, f'Todos os dados de {nome} foram excluídos permanentemente conforme solicitado (LGPD).')
        return redirect('lista_alunos')
    return render(request, 'alunos/confirmar_exclusao.html', {'aluno': aluno})