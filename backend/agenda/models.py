from django.db import models
from alunos.models import Aluno


class Aula(models.Model):
    SITUACAO_CHOICES = [
        ('agendada',  'Agendada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ]

    aluno        = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='aulas')
    data         = models.DateField()
    hora_inicio  = models.TimeField()
    hora_fim     = models.TimeField()
    observacoes  = models.TextField(blank=True, null=True)
    situacao     = models.CharField(max_length=20, choices=SITUACAO_CHOICES, default='agendada')
    criado_em    = models.DateTimeField(auto_now_add=True)
    atualizado_em= models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['data', 'hora_inicio']
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    def __str__(self):
        return f"{self.aluno.nome} — {self.data} {self.hora_inicio}"
