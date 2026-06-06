from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Aula


class AulaForm(forms.ModelForm):
    class Meta:
        model  = Aula
        fields = ['aluno', 'data', 'hora_inicio', 'hora_fim', 'observacoes', 'situacao']
        widgets = {
            'aluno':       forms.Select(attrs={'class': 'form-select'}),
            'data':        forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fim':    forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'situacao':    forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned = super().clean()
        data        = cleaned.get('data')
        hora_inicio = cleaned.get('hora_inicio')
        hora_fim    = cleaned.get('hora_fim')
        if hora_inicio and hora_fim and hora_fim <= hora_inicio:
            raise ValidationError('O horário de fim deve ser maior que o horário de início.')
        return cleaned
