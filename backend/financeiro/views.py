from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
from .models import Plano, Pagamento
from alunos.models import Aluno
from .forms import PlanoForm, PagamentoForm


@login_required
def lista_pagamentos(request):
    filtro = request.GET.get('filtro', 'todos')
    hoje   = date.today()
    pagamentos = Pagamento.objects.select_related('aluno', 'plano').order_by('-data_vencimento')
    if filtro == 'pendentes':
        pagamentos = pagamentos.filter(pago=False, data_vencimento__gte=hoje)
    elif filtro == 'pagos':
        pagamentos = pagamentos.filter(pago=True)
    elif filtro == 'vencidos':
        pagamentos = pagamentos.filter(pago=False, data_vencimento__lt=hoje)
    total_recebido = sum(p.valor for p in Pagamento.objects.filter(pago=True))
    total_pendente = sum(p.valor for p in Pagamento.objects.filter(pago=False))
    return render(request, 'financeiro/lista.html', {
        'pagamentos': pagamentos, 'filtro': filtro,
        'total_recebido': total_recebido, 'total_pendente': total_pendente, 'hoje': hoje,
    })


@login_required
def registrar_pagamento(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pag = form.save(commit=False)
            if pag.plano and (not pag.valor or pag.valor == 0):
                pag.valor = pag.plano.valor
            pag.save()
            messages.success(request, 'Pagamento registrado com sucesso!')
            return redirect('lista_pagamentos')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        aluno_id = request.GET.get('aluno')
        form = PagamentoForm(initial={'aluno': aluno_id} if aluno_id else {})
    return render(request, 'financeiro/form_pagamento.html', {'form': form, 'titulo': 'Registrar Pagamento'})


@login_required
def editar_pagamento(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento atualizado!')
            return redirect('lista_pagamentos')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = PagamentoForm(instance=pagamento)
    return render(request, 'financeiro/form_pagamento.html', {
        'form': form, 'titulo': 'Editar Pagamento', 'pagamento': pagamento
    })


@login_required
def marcar_pago(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    if request.method == 'POST':
        pagamento.pago           = True
        pagamento.data_pagamento = date.today()
        forma = request.POST.get('forma_pagamento')
        if forma:
            pagamento.forma_pagamento = forma
        pagamento.save()
        messages.success(request, f'Pagamento de {pagamento.aluno.nome} marcado como pago!')
    return redirect('lista_pagamentos')


@login_required
def lista_planos(request):
    planos = Plano.objects.filter(ativo=True)
    return render(request, 'financeiro/planos.html', {'planos': planos})


@login_required
def criar_plano(request):
    if request.method == 'POST':
        form = PlanoForm(request.POST)
        if form.is_valid():
            plano = form.save()
            messages.success(request, f'Plano "{plano.nome}" criado!')
            return redirect('lista_planos')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = PlanoForm()
    return render(request, 'financeiro/form_plano.html', {'form': form})


@login_required
def editar_plano(request, pk):
    plano = get_object_or_404(Plano, pk=pk)
    if request.method == 'POST':
        form = PlanoForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plano atualizado!')
            return redirect('lista_planos')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = PlanoForm(instance=plano)
    return render(request, 'financeiro/form_plano.html', {'form': form, 'plano': plano})


@login_required
def plano_aluno(request, aluno_pk):
    """Troca o plano de um aluno específico"""
    aluno = get_object_or_404(Aluno, pk=aluno_pk)
    planos = Plano.objects.filter(ativo=True)

    # Pagamento mais recente do aluno
    pagamento_atual = Pagamento.objects.filter(
        aluno=aluno, pago=False
    ).order_by('-criado_em').first()

    if request.method == 'POST':
        plano_id = request.POST.get('plano_id')
        data_vencimento = request.POST.get('data_vencimento')
        plano = get_object_or_404(Plano, pk=plano_id)

        Pagamento.objects.create(
            aluno=aluno,
            plano=plano,
            valor=plano.valor,
            data_vencimento=data_vencimento,
        )
        messages.success(request, f'Plano de {aluno.nome} atualizado para {plano.nome}!')
        return redirect('detalhe_aluno', pk=aluno_pk)

    return render(request, 'financeiro/plano_aluno.html', {
        'aluno': aluno,
        'planos': planos,
        'pagamento_atual': pagamento_atual,
    })


@login_required
def plano_valor(request, pk):
    plano = get_object_or_404(Plano, pk=pk)
    return JsonResponse({'valor': str(plano.valor)})
