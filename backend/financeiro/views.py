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
    hoje = date.today()
    pagamentos = Pagamento.objects.select_related('aluno', 'plano').order_by('-data_vencimento')

    if filtro == 'pendentes':
        pagamentos = pagamentos.filter(pago=False)
    elif filtro == 'pagos':
        pagamentos = pagamentos.filter(pago=True)
    elif filtro == 'vencidos':
        pagamentos = pagamentos.filter(pago=False, data_vencimento__lt=hoje)

    total_recebido = sum(p.valor for p in Pagamento.objects.filter(pago=True))
    total_pendente = sum(p.valor for p in Pagamento.objects.filter(pago=False))

    return render(request, 'financeiro/lista.html', {
        'pagamentos': pagamentos,
        'filtro': filtro,
        'total_recebido': total_recebido,
        'total_pendente': total_pendente,
        'hoje': hoje,
    })


@login_required
def registrar_pagamento(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pag = form.save(commit=False)
            # Definir valor do plano automaticamente
            if pag.plano:
                pag.valor = pag.plano.valor
            pag.save()
            messages.success(request, 'Pagamento registrado com sucesso!')
            return redirect('lista_pagamentos')
    else:
        aluno_id = request.GET.get('aluno')
        initial = {}
        if aluno_id:
            initial['aluno'] = aluno_id
        form = PagamentoForm(initial=initial)
    return render(request, 'financeiro/form_pagamento.html', {'form': form, 'titulo': 'Registrar Pagamento'})


@login_required
def marcar_pago(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    pagamento.pago = True
    pagamento.data_pagamento = date.today()
    if request.POST.get('forma_pagamento'):
        pagamento.forma_pagamento = request.POST.get('forma_pagamento')
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
        form = PlanoForm(instance=plano)
    return render(request, 'financeiro/form_plano.html', {'form': form, 'plano': plano})


@login_required
def plano_valor(request, pk):
    """API endpoint para retornar valor do plano via JS"""
    plano = get_object_or_404(Plano, pk=pk)
    return JsonResponse({'valor': str(plano.valor)})
