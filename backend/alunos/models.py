from django.db import models
from django.contrib.auth.models import User


class Aluno(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default='M')
    cep = models.CharField(max_length=9, blank=True)
    logradouro = models.CharField(max_length=200, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    objetivo = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class EvolutionFisica(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='evolucoes')
    data = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text='kg')
    altura = models.DecimalField(max_digits=4, decimal_places=2, help_text='metros')
    imc = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    percentual_gordura = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evolução Física'
        verbose_name_plural = 'Evoluções Físicas'
        ordering = ['-data']

    def save(self, *args, **kwargs):
        # calcula o IMC automaticamente antes de salvar, sem depender do formulário
        if self.peso and self.altura and self.altura > 0:
            self.imc = round(float(self.peso) / (float(self.altura) ** 2), 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.aluno.nome} - {self.data}'
