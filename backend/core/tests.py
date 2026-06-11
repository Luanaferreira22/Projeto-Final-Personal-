"""
Personal Manager — Testes Unitários Completos
PFC — Sistemas de Informação | UMC — Luana Ferreira — 2026

Como rodar:
    cd backend
    python manage.py test

Para ver cobertura:
    pip install coverage
    coverage run manage.py test
    coverage report
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from alunos.models import Aluno, EvolutionFisica
from treinos.models import Treino, Exercicio, TreinoExercicio
from financeiro.models import Plano, Pagamento
from agenda.models import Aula
from datetime import date, timedelta
import json


# ══════════════════════════════════════════════════════════════
# 1. TESTES DE AUTENTICAÇÃO
# ══════════════════════════════════════════════════════════════
class AutenticacaoTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.personal = User.objects.create_user(
            username='personal', password='senha123', is_staff=True
        )
        self.aluno_user = User.objects.create_user(
            username='aluno', password='senha123', is_staff=False
        )

    def test_login_personal_valido(self):
        """Personal trainer consegue logar com credenciais corretas"""
        response = self.client.post('/login/', {
            'username': 'personal', 'password': 'senha123'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_personal_invalido(self):
        """Login com senha errada retorna para tela de login"""
        response = self.client.post('/login/', {
            'username': 'personal', 'password': 'senhaerrada'
        })
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requer_login(self):
        """Dashboard redireciona para login se não autenticado"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_lista_alunos_requer_login(self):
        """Lista de alunos requer autenticação"""
        response = self.client.get('/alunos/')
        self.assertEqual(response.status_code, 302)

    def test_treinos_requer_login(self):
        """Lista de treinos requer autenticação"""
        response = self.client.get('/treinos/')
        self.assertEqual(response.status_code, 302)

    def test_financeiro_requer_login(self):
        """Financeiro requer autenticação"""
        response = self.client.get('/financeiro/')
        self.assertEqual(response.status_code, 302)

    def test_agenda_requer_login(self):
        """Agenda requer autenticação"""
        response = self.client.get('/agenda/')
        self.assertEqual(response.status_code, 302)

    def test_aluno_nao_acessa_dashboard(self):
        """Aluno não pode acessar dashboard do personal"""
        self.client.login(username='aluno', password='senha123')
        response = self.client.get('/')
        self.assertNotEqual(response.status_code, 200)

    def test_aluno_nao_acessa_lista_alunos(self):
        """Aluno não pode acessar lista de alunos"""
        self.client.login(username='aluno', password='senha123')
        response = self.client.get('/alunos/')
        self.assertNotEqual(response.status_code, 200)

    def test_logout_redireciona_para_login(self):
        """Logout redireciona para tela de login"""
        self.client.login(username='personal', password='senha123')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)


# ══════════════════════════════════════════════════════════════
# 2. TESTES DE ALUNOS
# ══════════════════════════════════════════════════════════════
class AlunoTest(TestCase):

    def setUp(self):
        self.personal = User.objects.create_user(
            username='personal', password='senha123', is_staff=True
        )
        self.client.login(username='personal', password='senha123')
        self.aluno = Aluno.objects.create(
            nome='Maria Silva',
            email='maria@teste.com',
            telefone='(11) 91111-1111',
            cidade='Mogi das Cruzes',
            estado='SP',
            ativo=True
        )

    def test_criar_aluno(self):
        """Aluno é criado corretamente no banco"""
        self.assertEqual(self.aluno.nome, 'Maria Silva')
        self.assertTrue(self.aluno.ativo)

    def test_listar_alunos_retorna_200(self):
        """Lista de alunos retorna status 200"""
        response = self.client.get('/alunos/')
        self.assertEqual(response.status_code, 200)

    def test_detalhe_aluno_retorna_200(self):
        """Detalhe do aluno retorna status 200"""
        response = self.client.get(f'/alunos/{self.aluno.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_inativar_aluno(self):
        """Inativar aluno muda ativo para False"""
        self.aluno.ativo = False
        self.aluno.save()
        self.assertFalse(Aluno.objects.get(pk=self.aluno.pk).ativo)

    def test_email_unico(self):
        """Dois alunos não podem ter o mesmo email"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Aluno.objects.create(
                nome='Outro Aluno',
                email='maria@teste.com',
                telefone='(11) 92222-2222'
            )

    def test_aluno_str(self):
        """Método __str__ retorna o nome do aluno"""
        self.assertEqual(str(self.aluno), 'Maria Silva')

    def test_buscar_aluno_por_nome(self):
        """Busca de aluno por nome funciona"""
        resultado = Aluno.objects.filter(nome__icontains='Maria')
        self.assertEqual(resultado.count(), 1)

    def test_pagina_cadastro_retorna_200(self):
        """Página de cadastro de aluno retorna 200"""
        response = self.client.get('/alunos/cadastrar/')
        self.assertEqual(response.status_code, 200)


# ══════════════════════════════════════════════════════════════
# 3. TESTES DE EVOLUÇÃO FÍSICA
# ══════════════════════════════════════════════════════════════
class EvolutionFisicaTest(TestCase):

    def setUp(self):
        self.aluno = Aluno.objects.create(
            nome='João Santos',
            email='joao@teste.com',
            telefone='(11) 92222-2222',
            ativo=True
        )

    def test_calculo_imc_automatico(self):
        """IMC é calculado automaticamente ao salvar"""
        ev = EvolutionFisica.objects.create(
            aluno=self.aluno,
            data=date.today(),
            peso=70.0,
            altura=1.75
        )
        imc_esperado = round(70.0 / (1.75 ** 2), 2)
        self.assertEqual(float(ev.imc), imc_esperado)

    def test_imc_formula_correta(self):
        """Fórmula IMC = peso / altura² está correta"""
        ev = EvolutionFisica(
            aluno=self.aluno,
            data=date.today(),
            peso=80.0,
            altura=1.80
        )
        ev.save()
        self.assertAlmostEqual(float(ev.imc), 24.69, places=1)

    def test_multiplas_evolucoes_por_aluno(self):
        """Aluno pode ter múltiplos registros de evolução"""
        EvolutionFisica.objects.create(aluno=self.aluno, data=date.today(), peso=70.0, altura=1.75)
        EvolutionFisica.objects.create(aluno=self.aluno, data=date.today() - timedelta(days=30), peso=72.0, altura=1.75)
        self.assertEqual(self.aluno.evolucoes.count(), 2)

    def test_evolucao_str(self):
        """Método __str__ da evolução retorna string correta"""
        ev = EvolutionFisica.objects.create(
            aluno=self.aluno, data=date.today(), peso=70.0, altura=1.75
        )
        self.assertIn('João Santos', str(ev))


# ══════════════════════════════════════════════════════════════
# 4. TESTES DE TREINOS
# ══════════════════════════════════════════════════════════════
class TreinoTest(TestCase):

    def setUp(self):
        self.personal = User.objects.create_user(
            username='personal', password='senha123', is_staff=True
        )
        self.client.login(username='personal', password='senha123')
        self.aluno = Aluno.objects.create(
            nome='Carlos Pereira',
            email='carlos@teste.com',
            telefone='(11) 94444-4444',
            ativo=True
        )
        self.exercicio = Exercicio.objects.create(
            nome='Supino Reto',
            grupo_muscular='peito'
        )

    def test_criar_treino(self):
        """Treino é criado e vinculado ao aluno"""
        treino = Treino.objects.create(
            aluno=self.aluno,
            nome='Treino A - Peito',
            descricao='Foco em peitoral'
        )
        self.assertEqual(treino.aluno, self.aluno)
        self.assertTrue(treino.ativo)

    def test_treino_vinculado_ao_aluno(self):
        """Treino aparece na lista do aluno"""
        Treino.objects.create(aluno=self.aluno, nome='Treino B', descricao='')
        self.assertEqual(self.aluno.treinos.count(), 1)

    def test_lista_treinos_retorna_200(self):
        """Lista de treinos retorna status 200"""
        response = self.client.get('/treinos/')
        self.assertEqual(response.status_code, 200)

    def test_criar_exercicio(self):
        """Exercício é criado corretamente"""
        self.assertEqual(self.exercicio.nome, 'Supino Reto')
        self.assertEqual(self.exercicio.grupo_muscular, 'peito')

    def test_adicionar_exercicio_ao_treino(self):
        """Exercício pode ser adicionado ao treino"""
        treino = Treino.objects.create(aluno=self.aluno, nome='Treino A', descricao='')
        TreinoExercicio.objects.create(
            treino=treino,
            exercicio=self.exercicio,
            series=3,
            repeticoes='12',
            descanso=60
        )
        self.assertEqual(treino.exercicios.count(), 1)

    def test_lista_exercicios_retorna_200(self):
        """Lista de exercícios retorna status 200"""
        response = self.client.get('/treinos/exercicios/')
        self.assertEqual(response.status_code, 200)


# ══════════════════════════════════════════════════════════════
# 5. TESTES FINANCEIROS
# ══════════════════════════════════════════════════════════════
class FinanceiroTest(TestCase):

    def setUp(self):
        self.personal = User.objects.create_user(
            username='personal', password='senha123', is_staff=True
        )
        self.client.login(username='personal', password='senha123')
        self.aluno = Aluno.objects.create(
            nome='Ana Oliveira',
            email='ana@teste.com',
            telefone='(11) 93333-3333',
            ativo=True
        )
        self.plano = Plano.objects.create(
            nome='Plano Mensal',
            valor=150.00,
            duracao=30
        )

    def test_criar_plano(self):
        """Plano é criado corretamente"""
        self.assertEqual(self.plano.nome, 'Plano Mensal')
        self.assertEqual(float(self.plano.valor), 150.00)

    def test_registrar_pagamento(self):
        """Pagamento é registrado corretamente"""
        pag = Pagamento.objects.create(
            aluno=self.aluno, plano=self.plano,
            valor=self.plano.valor,
            data_vencimento=date.today(), pago=False
        )
        self.assertFalse(pag.pago)
        self.assertEqual(float(pag.valor), 150.00)

    def test_marcar_pagamento_como_pago(self):
        """Pagamento pode ser marcado como pago"""
        pag = Pagamento.objects.create(
            aluno=self.aluno, plano=self.plano,
            valor=self.plano.valor,
            data_vencimento=date.today(), pago=False
        )
        pag.pago = True
        pag.data_pagamento = date.today()
        pag.save()
        self.assertTrue(Pagamento.objects.get(pk=pag.pk).pago)

    def test_lista_pagamentos_retorna_200(self):
        """Lista de pagamentos retorna 200"""
        response = self.client.get('/financeiro/')
        self.assertEqual(response.status_code, 200)

    def test_lista_planos_retorna_200(self):
        """Lista de planos retorna 200"""
        response = self.client.get('/financeiro/planos/')
        self.assertEqual(response.status_code, 200)

    def test_pagamento_vinculado_ao_aluno(self):
        """Pagamento aparece na lista do aluno"""
        Pagamento.objects.create(
            aluno=self.aluno, plano=self.plano,
            valor=self.plano.valor,
            data_vencimento=date.today()
        )
        self.assertEqual(self.aluno.pagamentos.count(), 1)

    def test_plano_str(self):
        """Método __str__ do plano retorna string correta"""
        self.assertIn('Plano Mensal', str(self.plano))


# ══════════════════════════════════════════════════════════════
# 6. TESTES DE AGENDA
# ══════════════════════════════════════════════════════════════
class AgendaTest(TestCase):

    def setUp(self):
        self.personal = User.objects.create_user(
            username='personal', password='senha123', is_staff=True
        )
        self.client.login(username='personal', password='senha123')
        self.aluno = Aluno.objects.create(
            nome='Fernanda Costa',
            email='fernanda@teste.com',
            telefone='(11) 95555-5555',
            ativo=True
        )

    def test_agendar_aula(self):
        """Aula é criada corretamente"""
        aula = Aula.objects.create(
            aluno=self.aluno,
            data=date.today() + timedelta(days=1),
            hora_inicio='08:00',
            hora_fim='09:00',
            situacao='agendada'
        )
        self.assertEqual(aula.situacao, 'agendada')
        self.assertEqual(aula.aluno, self.aluno)

    def test_cancelar_aula(self):
        """Aula pode ser cancelada"""
        aula = Aula.objects.create(
            aluno=self.aluno,
            data=date.today() + timedelta(days=1),
            hora_inicio='08:00',
            hora_fim='09:00',
            situacao='agendada'
        )
        aula.situacao = 'cancelada'
        aula.save()
        self.assertEqual(Aula.objects.get(pk=aula.pk).situacao, 'cancelada')

    def test_marcar_aula_realizada(self):
        """Aula pode ser marcada como realizada"""
        aula = Aula.objects.create(
            aluno=self.aluno,
            data=date.today(),
            hora_inicio='08:00',
            hora_fim='09:00',
            situacao='agendada'
        )
        aula.situacao = 'realizada'
        aula.save()
        self.assertEqual(Aula.objects.get(pk=aula.pk).situacao, 'realizada')

    def test_agenda_retorna_200(self):
        """Página da agenda retorna status 200"""
        response = self.client.get('/agenda/')
        self.assertEqual(response.status_code, 200)

    def test_aulas_futuras_do_aluno(self):
        """Filtro de aulas futuras funciona corretamente"""
        Aula.objects.create(
            aluno=self.aluno,
            data=date.today() + timedelta(days=1),
            hora_inicio='08:00', hora_fim='09:00', situacao='agendada'
        )
        Aula.objects.create(
            aluno=self.aluno,
            data=date.today() - timedelta(days=1),
            hora_inicio='08:00', hora_fim='09:00', situacao='realizada'
        )
        aulas_futuras = Aula.objects.filter(aluno=self.aluno, data__gte=date.today())
        self.assertEqual(aulas_futuras.count(), 1)

    def test_aula_str(self):
        """Método __str__ da aula retorna string correta"""
        aula = Aula.objects.create(
            aluno=self.aluno,
            data=date.today(),
            hora_inicio='08:00',
            hora_fim='09:00'
        )
        self.assertIn('Fernanda Costa', str(aula))
# ══════════════════════════════════════════════════════════════
# 7. TESTES DO FLUXO DO ALUNO (views_aluno.py)
# ══════════════════════════════════════════════════════════════
class FluxoAlunoTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_aluno = User.objects.create_user(
            username='mariasilva', password='senha123',
            email='maria@teste.com', is_staff=False
        )
        self.aluno = Aluno.objects.create(
            nome='Maria Silva',
            email='maria@teste.com',
            telefone='(11) 91111-1111',
            usuario=self.user_aluno,
            ativo=True
        )

    def test_pagina_login_aluno_retorna_200(self):
        """Tela de login do aluno carrega corretamente"""
        response = self.client.get('/aluno/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_aluno_sem_lgpd_falha(self):
        """Aluno nao loga sem aceitar a LGPD"""
        response = self.client.post('/aluno/login/', {
            'email': 'maria@teste.com',
            'password': 'senha123',
        })
        self.assertEqual(response.status_code, 200)
        self.aluno.refresh_from_db()
        self.assertFalse(self.aluno.aceite_lgpd)

    def test_login_aluno_com_lgpd_sucesso(self):
        """Aluno loga e o aceite LGPD e salvo no banco com data"""
        response = self.client.post('/aluno/login/', {
            'email': 'maria@teste.com',
            'password': 'senha123',
            'aceita_lgpd': 'on',
        })
        self.assertEqual(response.status_code, 302)
        self.aluno.refresh_from_db()
        self.assertTrue(self.aluno.aceite_lgpd)
        self.assertIsNotNone(self.aluno.data_aceite_lgpd)

    def test_login_aluno_senha_errada(self):
        """Login do aluno com senha errada falha"""
        response = self.client.post('/aluno/login/', {
            'email': 'maria@teste.com',
            'password': 'senhaerrada',
            'aceita_lgpd': 'on',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_aluno_email_inexistente(self):
        """Login com email nao cadastrado falha"""
        response = self.client.post('/aluno/login/', {
            'email': 'naoexiste@teste.com',
            'password': 'senha123',
            'aceita_lgpd': 'on',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_aluno_sem_campos(self):
        """Login sem email e senha exibe erro"""
        response = self.client.post('/aluno/login/', {
            'email': '', 'password': '', 'aceita_lgpd': 'on',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_aluno_sem_usuario_vinculado(self):
        """Aluno sem usuario Django nao consegue logar"""
        Aluno.objects.create(
            nome='Sem Login', email='semlogin@teste.com',
            telefone='(11) 90000-0000', ativo=True
        )
        response = self.client.post('/aluno/login/', {
            'email': 'semlogin@teste.com',
            'password': 'qualquer',
            'aceita_lgpd': 'on',
        })
        self.assertEqual(response.status_code, 200)

    def test_painel_aluno_requer_login(self):
        """Painel do aluno redireciona se nao autenticado"""
        response = self.client.get('/aluno/painel/')
        self.assertEqual(response.status_code, 302)

    def test_painel_aluno_logado_retorna_200(self):
        """Aluno logado acessa o painel"""
        self.client.login(username='mariasilva', password='senha123')
        response = self.client.get('/aluno/painel/')
        self.assertEqual(response.status_code, 200)

    def test_personal_redirecionado_do_painel_aluno(self):
        """Personal e redirecionado ao tentar acessar painel do aluno"""
        User.objects.create_user(username='pt', password='senha123', is_staff=True)
        self.client.login(username='pt', password='senha123')
        response = self.client.get('/aluno/painel/')
        self.assertEqual(response.status_code, 302)

    def test_logout_aluno(self):
        """Logout do aluno redireciona"""
        self.client.login(username='mariasilva', password='senha123')
        response = self.client.get('/aluno/logout/')
        self.assertEqual(response.status_code, 302)


# ══════════════════════════════════════════════════════════════
# 8. TESTES DE TROCA DE SENHA DO ALUNO
# ══════════════════════════════════════════════════════════════
class AlterarSenhaAlunoTest(TestCase):

    def setUp(self):
        self.user_aluno = User.objects.create_user(
            username='joaosantos', password='senhaantiga',
            email='joao@teste.com', is_staff=False
        )
        self.aluno = Aluno.objects.create(
            nome='Joao Santos', email='joao@teste.com',
            telefone='(11) 92222-2222',
            usuario=self.user_aluno, ativo=True
        )
        self.client.login(username='joaosantos', password='senhaantiga')

    def test_pagina_alterar_senha_retorna_200(self):
        """Tela de alterar senha carrega"""
        response = self.client.get('/aluno/alterar-senha/')
        self.assertEqual(response.status_code, 200)

    def test_alterar_senha_sucesso(self):
        """Aluno troca a senha com dados validos"""
        response = self.client.post('/aluno/alterar-senha/', {
            'senha_atual': 'senhaantiga',
            'nova_senha': 'novasenha456',
            'confirmar_senha': 'novasenha456',
        })
        self.assertEqual(response.status_code, 302)
        self.user_aluno.refresh_from_db()
        self.assertTrue(self.user_aluno.check_password('novasenha456'))

    def test_alterar_senha_atual_errada(self):
        """Senha atual incorreta impede a troca"""
        response = self.client.post('/aluno/alterar-senha/', {
            'senha_atual': 'errada',
            'nova_senha': 'novasenha456',
            'confirmar_senha': 'novasenha456',
        })
        self.assertEqual(response.status_code, 200)
        self.user_aluno.refresh_from_db()
        self.assertTrue(self.user_aluno.check_password('senhaantiga'))

    def test_alterar_senha_curta(self):
        """Nova senha com menos de 6 caracteres e rejeitada"""
        response = self.client.post('/aluno/alterar-senha/', {
            'senha_atual': 'senhaantiga',
            'nova_senha': '123',
            'confirmar_senha': '123',
        })
        self.assertEqual(response.status_code, 200)

    def test_alterar_senha_confirmacao_diferente(self):
        """Confirmacao diferente da nova senha e rejeitada"""
        response = self.client.post('/aluno/alterar-senha/', {
            'senha_atual': 'senhaantiga',
            'nova_senha': 'novasenha456',
            'confirmar_senha': 'outracoisa789',
        })
        self.assertEqual(response.status_code, 200)

    def test_alterar_senha_igual_atual(self):
        """Nova senha igual a atual e rejeitada"""
        response = self.client.post('/aluno/alterar-senha/', {
            'senha_atual': 'senhaantiga',
            'nova_senha': 'senhaantiga',
            'confirmar_senha': 'senhaantiga',
        })
        self.assertEqual(response.status_code, 200)

    def test_alterar_senha_requer_login(self):
        """Tela de alterar senha exige autenticacao"""
        self.client.logout()
        response = self.client.get('/aluno/alterar-senha/')
        self.assertEqual(response.status_code, 302)


# ══════════════════════════════════════════════════════════════
# 9. TESTES DAS PAGINAS DO PERSONAL (GET das views)
# ══════════════════════════════════════════════════════════════
class PaginasPersonalTest(TestCase):

    def setUp(self):
        self.personal = User.objects.create_user(
            username='personal', password='senha123', is_staff=True
        )
        self.client.login(username='personal', password='senha123')
        self.aluno = Aluno.objects.create(
            nome='Carla Souza', email='carla@teste.com',
            telefone='(11) 96666-6666', ativo=True
        )
        self.plano = Plano.objects.create(nome='Plano Teste', valor=100.00, duracao=30)
        self.treino = Treino.objects.create(aluno=self.aluno, nome='Treino X', descricao='')
        self.aula = Aula.objects.create(
            aluno=self.aluno, data=date.today() + timedelta(days=1),
            hora_inicio='10:00', hora_fim='11:00', situacao='agendada'
        )

    def test_dashboard_logado_retorna_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_login_retorna_200(self):
        self.client.logout()
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_politica_privacidade_retorna_200(self):
        response = self.client.get('/politica-privacidade/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_editar_aluno_retorna_200(self):
        response = self.client.get(f'/alunos/{self.aluno.pk}/editar/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_evolucao_retorna_200(self):
        response = self.client.get(f'/alunos/{self.aluno.pk}/evolucao/')
        self.assertEqual(response.status_code, 200)

    def test_inativar_aluno_via_url(self):
        response = self.client.get(f'/alunos/{self.aluno.pk}/inativar/')
        self.assertEqual(response.status_code, 302)
        self.aluno.refresh_from_db()
        self.assertFalse(self.aluno.ativo)

    def test_pagina_criar_treino_retorna_200(self):
        response = self.client.get('/treinos/criar/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_detalhe_treino_retorna_200(self):
        response = self.client.get(f'/treinos/{self.treino.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_registrar_pagamento_retorna_200(self):
        response = self.client.get('/financeiro/registrar/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_criar_plano_retorna_200(self):
        response = self.client.get('/financeiro/planos/criar/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_editar_plano_retorna_200(self):
        response = self.client.get(f'/financeiro/planos/{self.plano.pk}/editar/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_plano_aluno_retorna_200(self):
        response = self.client.get(f'/financeiro/plano-aluno/{self.aluno.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_api_plano_valor_retorna_json(self):
        """Endpoint do valor do plano retorna JSON com o valor"""
        response = self.client.get(f'/financeiro/planos/valor/{self.plano.pk}/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['valor'], '100.00')

    def test_marcar_pagamento_pago_via_url(self):
        pag = Pagamento.objects.create(
            aluno=self.aluno, plano=self.plano, valor=100.00,
            data_vencimento=date.today(), pago=False
        )
        response = self.client.post(f'/financeiro/{pag.pk}/pago/')
        self.assertEqual(response.status_code, 302)
        pag.refresh_from_db()
        self.assertTrue(pag.pago)

    def test_pagina_agendar_aula_retorna_200(self):
        response = self.client.get('/agenda/agendar/')
        self.assertEqual(response.status_code, 200)

    def test_pagina_editar_aula_retorna_200(self):
        response = self.client.get(f'/agenda/editar/{self.aula.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_cancelar_aula_via_url(self):
        response = self.client.get(f'/agenda/cancelar/{self.aula.pk}/')
        self.assertEqual(response.status_code, 302)
        self.aula.refresh_from_db()
        self.assertEqual(self.aula.situacao, 'cancelada')

    def test_agenda_com_filtro_aluno(self):
        response = self.client.get(f'/agenda/?aluno={self.aluno.pk}')
        self.assertEqual(response.status_code, 200)

    def test_agenda_navegacao_semana(self):
        proxima = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')
        response = self.client.get(f'/agenda/?semana={proxima}')
        self.assertEqual(response.status_code, 200)

    def test_lista_alunos_com_busca(self):
        response = self.client.get('/alunos/?q=Carla')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carla')

    def test_lista_treinos_com_filtro(self):
        response = self.client.get(f'/treinos/?aluno={self.aluno.pk}')
        self.assertEqual(response.status_code, 200)
