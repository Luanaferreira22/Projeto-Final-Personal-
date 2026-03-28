from django import forms
from .models import Plano, Pagamento


class PlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields = ['nome', 'valor', 'duracao', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Plano Mensal'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '150.00'}),
            'duracao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 30'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['aluno', 'plano', 'valor', 'data_vencimento', 'pago', 'forma_pagamento', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'plano': forms.Select(attrs={'class': 'form-select', 'id': 'id_plano'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'id': 'id_valor'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pago': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
