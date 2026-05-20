from django.db import models
from alunos.models import Aluno

class Plano(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    duracao = models.PositiveIntegerField(help_text='Duração em dias')
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['valor']

    def __str__(self):
        return f'{self.nome} - R$ {self.valor}'

class Pagamento(models.Model):
    FORMA_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('pix', 'PIX'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('transferencia', 'Transferência'),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='pagamentos')
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    pago = models.BooleanField(default=False)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_CHOICES, blank=True)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data_vencimento']

    def __str__(self):
        status = 'Pago' if self.pago else 'Pendente'
        return f'{self.aluno.nome} - {self.plano} - {status}'
