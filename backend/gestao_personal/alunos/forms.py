from django import forms
from django.core.exceptions import ValidationError
from .models import Aluno, EvolutionFisica
import re


class AlunoForm(forms.ModelForm):
    consentimento_lgpd = forms.BooleanField(
        required=True,
        label='Concordo com o uso dos meus dados pessoais conforme a Política de Privacidade (LGPD — Lei nº 13.709/2018)',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_consentimento_lgpd'}),
        error_messages={'required': 'É necessário aceitar a Política de Privacidade para cadastrar o aluno.'}
    )

    class Meta:
        model = Aluno
        fields = [
            'nome', 'email', 'telefone', 'data_nascimento',
            'sexo', 'cep', 'logradouro', 'bairro', 'cidade', 'estado', 'objetivo'
        ]
        widgets = {
            'nome':            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'email':           forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'telefone':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999', 'id': 'id_telefone'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo':            forms.Select(attrs={'class': 'form-select'}),
            'cep':             forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000', 'id': 'id_cep', 'maxlength': '9'}),
            'logradouro':      forms.TextInput(attrs={'class': 'form-control', 'id': 'id_logradouro'}),
            'bairro':          forms.TextInput(attrs={'class': 'form-control', 'id': 'id_bairro'}),
            'cidade':          forms.TextInput(attrs={'class': 'form-control', 'id': 'id_cidade'}),
            'estado':          forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2', 'id': 'id_estado'}),
            'objetivo':        forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva o objetivo do aluno...'}),
        }

    def __init__(self, *args, **kwargs):
        self.instance_pk = kwargs.get('instance').pk if kwargs.get('instance') else None
        super().__init__(*args, **kwargs)
        self.fields['objetivo'].required     = False
        self.fields['cep'].required          = False
        self.fields['logradouro'].required   = False
        self.fields['bairro'].required       = False
        self.fields['cidade'].required       = False
        self.fields['estado'].required       = False
        if self.instance_pk:
            self.fields['consentimento_lgpd'].required = False
            self.fields['consentimento_lgpd'].initial  = True

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        if len(nome) < 3:
            raise ValidationError('O nome deve ter pelo menos 3 caracteres.')
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome):
            raise ValidationError('O nome deve conter apenas letras e espaços.')
        return nome

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        qs = Aluno.objects.filter(email=email)
        if self.instance_pk:
            qs = qs.exclude(pk=self.instance_pk)
        if qs.exists():
            raise ValidationError('Já existe um aluno cadastrado com este e-mail.')
        return email

    def clean_telefone(self):
        tel    = self.cleaned_data.get('telefone', '').strip()
        digits = re.sub(r'\D', '', tel)
        if len(digits) < 10:
            raise ValidationError('Telefone inválido. Informe DDD + número (mínimo 10 dígitos).')
        if len(digits) > 11:
            raise ValidationError('Telefone inválido. Máximo 11 dígitos.')
        return tel

    def clean_cep(self):
        cep = self.cleaned_data.get('cep', '').strip()
        if cep:
            digits = re.sub(r'\D', '', cep)
            if len(digits) != 8:
                raise ValidationError('CEP inválido. Informe 8 dígitos.')
        return cep

    def clean_estado(self):
        estado = self.cleaned_data.get('estado', '').strip().upper()
        ufs_validas = [
            'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA',
            'MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN',
            'RS','RO','RR','SC','SP','SE','TO'
        ]
        if estado and estado not in ufs_validas:
            raise ValidationError('UF inválida. Informe a sigla do estado (ex: SP).')
        return estado


class EvolutionFisicaForm(forms.ModelForm):
    class Meta:
        model  = EvolutionFisica
        fields = ['data', 'peso', 'altura', 'percentual_gordura', 'observacoes']
        widgets = {
            'data':               forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'peso':               forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 70.5', 'min': '20', 'max': '300'}),
            'altura':             forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 1.75', 'min': '0.5', 'max': '2.5'}),
            'percentual_gordura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Ex: 18.5', 'min': '1', 'max': '70'}),
            'observacoes':        forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso and (peso < 20 or peso > 300):
            raise ValidationError('Peso inválido. Informe entre 20 e 300 kg.')
        return peso

    def clean_altura(self):
        altura = self.cleaned_data.get('altura')
        if altura and (altura < 0.5 or altura > 2.5):
            raise ValidationError('Altura inválida. Informe entre 0,50 e 2,50 m.')
        return altura
