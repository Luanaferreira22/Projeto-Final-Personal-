from django.db import models
from alunos.models import Aluno


class Exercicio(models.Model):
    GRUPO_CHOICES = [
        ('peito', 'Peito'),
        ('costas', 'Costas'),
        ('ombros', 'Ombros'),
        ('biceps', 'Bíceps'),
        ('triceps', 'Tríceps'),
        ('abdomen', 'Abdômen'),
        ('gluteos', 'Glúteos'),
        ('quadriceps', 'Quadríceps'),
        ('posterior', 'Posterior de coxa'),
        ('panturrilha', 'Panturrilha'),
        ('cardio', 'Cardio'),
        ('outros', 'Outros'),
    ]
    nome = models.CharField(max_length=100)
    grupo_muscular = models.CharField(max_length=20, choices=GRUPO_CHOICES, default='outros')
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Exercício'
        verbose_name_plural = 'Exercícios'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.get_grupo_muscular_display()})'


class Treino(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='treinos')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Treino'
        verbose_name_plural = 'Treinos'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} - {self.aluno.nome}'


class TreinoExercicio(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='exercicios')
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    series = models.PositiveIntegerField(default=3)
    repeticoes = models.CharField(max_length=20, default='12', help_text='Ex: 12 ou 8-12')
    carga = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='kg')
    descanso = models.PositiveIntegerField(default=60, help_text='segundos')
    observacoes = models.TextField(blank=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Exercício do Treino'
        verbose_name_plural = 'Exercícios do Treino'
        ordering = ['ordem']

    def __str__(self):
        return f'{self.exercicio.nome} - {self.treino.nome}'
