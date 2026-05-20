from django import forms
from django.core.exceptions import ValidationError
from .models import Treino, TreinoExercicio, Exercicio


class TreinoForm(forms.ModelForm):
    class Meta:
        model  = Treino
        fields = ['aluno', 'nome', 'descricao']
        widgets = {
            'aluno':     forms.Select(attrs={'class': 'form-select'}),
            'nome':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Treino A — Peito e Tríceps'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        if len(nome) < 3:
            raise ValidationError('O nome do treino deve ter pelo menos 3 caracteres.')
        return nome


class TreinoExercicioForm(forms.ModelForm):
    class Meta:
        model  = TreinoExercicio
        fields = ['exercicio', 'series', 'repeticoes', 'carga', 'descanso', 'observacoes']
        widgets = {
            'exercicio':   forms.Select(attrs={'class': 'form-select'}),
            'series':      forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '20'}),
            'repeticoes':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12 ou 8-12'}),
            'carga':       forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'placeholder': 'kg', 'min': '0'}),
            'descanso':    forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'segundos', 'min': '0', 'max': '600'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_series(self):
        series = self.cleaned_data.get('series')
        if series and (series < 1 or series > 20):
            raise ValidationError('O número de séries deve ser entre 1 e 20.')
        return series


class ExercicioForm(forms.ModelForm):
    class Meta:
        model  = Exercicio
        fields = ['nome', 'grupo_muscular', 'descricao']
        widgets = {
            'nome':           forms.TextInput(attrs={'class': 'form-control'}),
            'grupo_muscular': forms.Select(attrs={'class': 'form-select'}),
            'descricao':      forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        if len(nome) < 3:
            raise ValidationError('O nome do exercício deve ter pelo menos 3 caracteres.')
        if Exercicio.objects.filter(nome__iexact=nome).exclude(
                pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError('Já existe um exercício com este nome.')
        return nome
