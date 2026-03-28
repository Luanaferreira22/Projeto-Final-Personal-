from django import forms
from .models import Treino, TreinoExercicio, Exercicio


class TreinoForm(forms.ModelForm):
    class Meta:
        model = Treino
        fields = ['aluno', 'nome', 'descricao']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Treino A - Peito e Tríceps'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TreinoExercicioForm(forms.ModelForm):
    class Meta:
        model = TreinoExercicio
        fields = ['exercicio', 'series', 'repeticoes', 'carga', 'descanso', 'observacoes']
        widgets = {
            'exercicio': forms.Select(attrs={'class': 'form-select'}),
            'series': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'repeticoes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12 ou 8-12'}),
            'carga': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'placeholder': 'kg'}),
            'descanso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'segundos'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ExercicioForm(forms.ModelForm):
    class Meta:
        model = Exercicio
        fields = ['nome', 'grupo_muscular', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'grupo_muscular': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
