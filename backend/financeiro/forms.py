from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Plano, Pagamento


class PlanoForm(forms.ModelForm):
    class Meta:
        model = Plano
        fields = ['nome', 'valor', 'duracao', 'descricao']
        widgets = {
            'nome':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Plano Mensal'}),
            'valor':     forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '150.00', 'min': '1'}),
            'duracao':   forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 30', 'min': '1', 'max': '365'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor and valor <= 0:
            raise ValidationError('O valor do plano deve ser maior que zero.')
        return valor

    def clean_duracao(self):
        duracao = self.cleaned_data.get('duracao')
        if duracao and (duracao < 1 or duracao > 365):
            raise ValidationError('A duração deve ser entre 1 e 365 dias.')
        return duracao


class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['aluno', 'plano', 'valor', 'data_vencimento', 'pago', 'forma_pagamento', 'observacoes']
        widgets = {
            'aluno':           forms.Select(attrs={'class': 'form-select'}),
            'plano':           forms.Select(attrs={'class': 'form-select', 'id': 'id_plano'}),
            'valor':           forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'id': 'id_valor', 'min': '0.01'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pago':            forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-select'}),
            'observacoes':     forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise ValidationError('O valor deve ser maior que zero.')
        return valor

    def clean_data_vencimento(self):
        data_venc = self.cleaned_data.get('data_vencimento')
        if data_venc and data_venc < date.today():
            raise ValidationError('A data de vencimento não pode ser anterior a hoje.')
        return data_venc

    def clean(self):
        cleaned = super().clean()
        plano   = cleaned.get('plano')
        valor   = cleaned.get('valor')
        if plano and not valor:
            cleaned['valor'] = plano.valor
        return cleaned
