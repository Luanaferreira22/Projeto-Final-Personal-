"""
Script para popular o banco de dados com dados iniciais.
Execute com: python popular_db.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_personal.settings')
django.setup()

from django.contrib.auth.models import User
from treinos.models import Exercicio
from financeiro.models import Plano

# ─── Superusuário ───────────────────────────────────────────────────────────
if not User.objects.filter(username='personal').exists():
    User.objects.create_superuser(
        username='personal',
        email='personal@personal.com',
        password='personal123',
        first_name='Personal',
        last_name='Trainer'
    )
    print('✅ Superusuário criado: personal / personal123')
else:
    print('ℹ️  Superusuário já existe.')

# ─── Planos ──────────────────────────────────────────────────────────────────
planos = [
    {'nome': 'Plano Mensal',    'valor': 150.00, 'duracao': 30,  'descricao': '1 mês de acompanhamento'},
    {'nome': 'Plano Trimestral','valor': 400.00, 'duracao': 90,  'descricao': '3 meses com desconto'},
    {'nome': 'Plano Semestral', 'valor': 700.00, 'duracao': 180, 'descricao': '6 meses com maior desconto'},
    {'nome': 'Plano Anual',     'valor': 1200.00,'duracao': 365, 'descricao': '12 meses - melhor custo-benefício'},
]
for p in planos:
    obj, created = Plano.objects.get_or_create(nome=p['nome'], defaults=p)
    if created:
        print(f'✅ Plano criado: {obj.nome}')

# ─── Exercícios ──────────────────────────────────────────────────────────────
exercicios = [
    # Peito
    ('Supino Reto com Barra',       'peito'),
    ('Supino Inclinado com Halteres','peito'),
    ('Crucifixo',                   'peito'),
    ('Peck Deck',                   'peito'),
    # Costas
    ('Puxada Frontal',              'costas'),
    ('Remada Curvada',              'costas'),
    ('Remada Unilateral',           'costas'),
    ('Levantamento Terra',          'costas'),
    # Ombros
    ('Desenvolvimento com Barra',   'ombros'),
    ('Elevação Lateral',            'ombros'),
    ('Elevação Frontal',            'ombros'),
    # Bíceps
    ('Rosca Direta',                'biceps'),
    ('Rosca Alternada',             'biceps'),
    ('Rosca Concentrada',           'biceps'),
    # Tríceps
    ('Tríceps Pulley',              'triceps'),
    ('Tríceps Testa',               'triceps'),
    ('Mergulho no Banco',           'triceps'),
    # Abdômen
    ('Abdominal Crunch',            'abdomen'),
    ('Prancha',                     'abdomen'),
    ('Abdominal Oblíquo',           'abdomen'),
    # Glúteos
    ('Agachamento',                 'gluteos'),
    ('Stiff',                       'gluteos'),
    ('Passada (Lunge)',              'gluteos'),
    ('Elevação Pélvica',            'gluteos'),
    # Quadríceps
    ('Leg Press',                   'quadriceps'),
    ('Extensora',                   'quadriceps'),
    ('Agachamento Hack',            'quadriceps'),
    # Posterior
    ('Flexora',                     'posterior'),
    ('Mesa Flexora',                'posterior'),
    # Panturrilha
    ('Panturrilha em Pé',           'panturrilha'),
    ('Panturrilha Sentado',         'panturrilha'),
    # Cardio
    ('Esteira',                     'cardio'),
    ('Bicicleta Ergométrica',       'cardio'),
    ('Elíptico',                    'cardio'),
    ('Corda',                       'cardio'),
]
count = 0
for nome, grupo in exercicios:
    _, created = Exercicio.objects.get_or_create(nome=nome, defaults={'grupo_muscular': grupo})
    if created:
        count += 1
print(f'✅ {count} exercícios criados.')

print('\n🎉 Banco de dados populado com sucesso!')
print('━' * 40)
print('Login: personal')
print('Senha: personal123')
print('URL:   http://127.0.0.1:8000/')
