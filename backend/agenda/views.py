from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta, datetime
from .models import Aula
from .forms import AulaForm
from alunos.models import Aluno


@login_required
def agenda_personal(request):
    hoje = date.today()

    # Calcular semana a exibir
    semana_str = request.GET.get('semana', '')
    try:
        semana_inicio = datetime.strptime(semana_str, '%Y-%m-%d').date()
        # Garantir que começa na segunda-feira
        semana_inicio = semana_inicio - timedelta(days=semana_inicio.weekday())
    except (ValueError, TypeError):
        semana_inicio = hoje - timedelta(days=hoje.weekday())

    semana_fim = semana_inicio + timedelta(days=6)

    # Navegação
    semana_anterior = semana_inicio - timedelta(days=7)
    proxima_semana  = semana_inicio + timedelta(days=7)

    # Filtro por aluno
    aluno_filtro = request.GET.get('aluno', '')

    # Buscar aulas da semana
    aulas_semana = Aula.objects.select_related('aluno').filter(
        data__range=[semana_inicio, semana_fim]
    )
    if aluno_filtro:
        aulas_semana = aulas_semana.filter(aluno_id=aluno_filtro)

    # Montar estrutura dos 7 dias
    DIAS_PT = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    dias_semana = []
    for i in range(7):
        dia_data = semana_inicio + timedelta(days=i)
        aulas_dia = [a for a in aulas_semana if a.data == dia_data]
        dias_semana.append({
            'data':  dia_data,
            'nome':  DIAS_PT[i],
            'hoje':  dia_data == hoje,
            'aulas': sorted(aulas_dia, key=lambda a: a.hora_inicio),
            'total': len(aulas_dia),
        })

    # Horas a exibir (6h às 21h)
    horas = list(range(6, 22))

    # Aulas de hoje para o resumo
    aulas_hoje = [a for a in aulas_semana if a.data == hoje]

    alunos = Aluno.objects.filter(ativo=True).order_by('nome')

    return render(request, 'agenda/agenda_personal.html', {
        'dias_semana':     dias_semana,
        'horas':           horas,
        'hoje':            hoje,
        'semana_inicio':   semana_inicio,
        'semana_fim':      semana_fim,
        'semana_anterior': semana_anterior.strftime('%Y-%m-%d'),
        'proxima_semana':  proxima_semana.strftime('%Y-%m-%d'),
        'alunos':          alunos,
        'aluno_filtro':    aluno_filtro,
        'aulas_hoje':      aulas_hoje,
    })


@login_required
def agendar_aula(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aula agendada com sucesso!')
            return redirect('agenda_personal')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        aluno_id = request.GET.get('aluno')
        initial  = {'aluno': aluno_id} if aluno_id else {}
        form = AulaForm(initial=initial)
    return render(request, 'agenda/form_aula.html', {
        'form': form, 'titulo': 'Agendar Aula'
    })


@login_required
def editar_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    if request.method == 'POST':
        form = AulaForm(request.POST, instance=aula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aula atualizada!')
            return redirect('agenda_personal')
    else:
        form = AulaForm(instance=aula)
    return render(request, 'agenda/form_aula.html', {
        'form': form, 'titulo': 'Editar Aula', 'aula': aula
    })


@login_required
def cancelar_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    aula.situacao = 'cancelada'
    aula.save()
    messages.success(request, 'Aula cancelada.')
    return redirect('agenda_personal')


def agenda_aluno(request):
    if not request.user.is_authenticated:
        return redirect('login_aluno')
    try:
        aluno = Aluno.objects.get(usuario=request.user)
    except Aluno.DoesNotExist:
        return redirect('login_aluno')
    hoje  = date.today()
    aulas = Aula.objects.filter(aluno=aluno, data__gte=hoje).order_by('data', 'hora_inicio')
    aulas_passadas = Aula.objects.filter(aluno=aluno, data__lt=hoje).order_by('-data')[:5]
    return render(request, 'agenda/agenda_aluno.html', {
        'aluno': aluno, 'aulas': aulas,
        'aulas_passadas': aulas_passadas, 'hoje': hoje,
    })
