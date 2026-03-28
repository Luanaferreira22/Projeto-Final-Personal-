from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Treino, Exercicio, TreinoExercicio
from alunos.models import Aluno
from .forms import TreinoForm, TreinoExercicioForm, ExercicioForm


@login_required
def lista_treinos(request):
    treinos = Treino.objects.filter(ativo=True).select_related('aluno')
    aluno_id = request.GET.get('aluno')
    if aluno_id:
        treinos = treinos.filter(aluno_id=aluno_id)
    alunos = Aluno.objects.filter(ativo=True)
    return render(request, 'treinos/lista.html', {'treinos': treinos, 'alunos': alunos})


@login_required
def criar_treino(request):
    if request.method == 'POST':
        form = TreinoForm(request.POST)
        if form.is_valid():
            treino = form.save()
            messages.success(request, f'Treino "{treino.nome}" criado com sucesso!')
            return redirect('detalhe_treino', pk=treino.pk)
    else:
        aluno_id = request.GET.get('aluno')
        initial = {}
        if aluno_id:
            initial['aluno'] = aluno_id
        form = TreinoForm(initial=initial)
    alunos = Aluno.objects.filter(ativo=True)
    return render(request, 'treinos/form.html', {'form': form, 'titulo': 'Criar Treino', 'alunos': alunos})


@login_required
def detalhe_treino(request, pk):
    treino = get_object_or_404(Treino, pk=pk)
    exercicios_treino = treino.exercicios.all().select_related('exercicio')
    form = TreinoExercicioForm()
    return render(request, 'treinos/detalhe.html', {
        'treino': treino,
        'exercicios_treino': exercicios_treino,
        'form': form,
    })


@login_required
def adicionar_exercicio_treino(request, pk):
    treino = get_object_or_404(Treino, pk=pk)
    if request.method == 'POST':
        form = TreinoExercicioForm(request.POST)
        if form.is_valid():
            te = form.save(commit=False)
            te.treino = treino
            te.ordem = treino.exercicios.count() + 1
            te.save()
            messages.success(request, 'Exercício adicionado ao treino!')
        else:
            messages.error(request, 'Erro ao adicionar exercício.')
    return redirect('detalhe_treino', pk=pk)


@login_required
def remover_exercicio_treino(request, pk, ex_pk):
    te = get_object_or_404(TreinoExercicio, pk=ex_pk, treino_id=pk)
    te.delete()
    messages.success(request, 'Exercício removido do treino.')
    return redirect('detalhe_treino', pk=pk)


@login_required
def lista_exercicios(request):
    exercicios = Exercicio.objects.all()
    return render(request, 'treinos/exercicios.html', {'exercicios': exercicios})


@login_required
def criar_exercicio(request):
    if request.method == 'POST':
        form = ExercicioForm(request.POST)
        if form.is_valid():
            ex = form.save()
            messages.success(request, f'Exercício "{ex.nome}" cadastrado!')
            return redirect('lista_exercicios')
    else:
        form = ExercicioForm()
    return render(request, 'treinos/exercicio_form.html', {'form': form})
