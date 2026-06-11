# Personal Manager — Gestao de Treinos para Personal Trainer

**TCC — Sistemas de Informacao | UMC — Luana Ferreira — 2026**

> Sistema desenvolvido com foco no **personal trainer autonomo**.

Sistema web para personal trainers gerenciarem alunos, treinos, agenda e controle financeiro.

---

## AVISO IMPORTANTE — Ambiente de Execucao

**Este sistema foi desenvolvido com foco no personal trainer autonomo,
para execucao em ambiente LOCAL (desenvolvimento), sem deploy em producao.**

- O servidor utilizado e o servidor de desenvolvimento do Django (`runserver`)
- O banco SQLite e adequado para o porte do sistema e uso local
- A evolucao para ambiente de producao esta documentada como trabalho futuro na monografia

---

## Pre-requisitos

| Requisito | Versao |
|-----------|--------|
| Python    | 3.11 ou superior |
| pip       | incluso no Python |
| Navegador | Chrome, Edge ou Firefox atualizados |

Para verificar se o Python esta instalado:

```bash
python --version
```

---

## Como executar o projeto (passo a passo)

### 1. Clonar ou baixar o repositorio

```bash
git clone https://github.com/Luanaferreira22/Projeto-Final-Personal-.git
cd Projeto-Final-Personal-
```

Ou baixe o ZIP pelo GitHub (Code > Download ZIP) e extraia.

### 2. Instalar as dependencias

```bash
pip install django==4.2.7 Pillow==10.1.0
```

### 3. Entrar na pasta backend

```bash
cd backend
```

### 4. Aplicar as migracoes (cria as tabelas do banco)

```bash
python manage.py migrate
```

### 5. Criar o usuario do personal trainer

```bash
python manage.py createsuperuser
```

Preencha usuario, email e senha quando solicitado.

### 6. Iniciar o servidor de desenvolvimento

```bash
python manage.py runserver
```

### 7. Acessar no navegador

```
http://127.0.0.1:8000/
```

Para encerrar o servidor: `CTRL+C` no terminal.

---

## Como rodar os testes unitarios

```bash
cd backend
python manage.py test
```

Para verificar a cobertura de testes:

```bash
pip install coverage
coverage run manage.py test
coverage report
```

---

## Acessos do sistema

| Tipo             | URL                                |
|------------------|------------------------------------|
| Personal Trainer | http://127.0.0.1:8000/login/       |
| Aluno            | http://127.0.0.1:8000/aluno/login/ |
| Agenda           | http://127.0.0.1:8000/agenda/      |

**Fluxo de acesso do aluno:** ao ser cadastrado pelo personal, o sistema gera
uma **senha temporaria aleatoria** exibida na tela. O personal repassa ao aluno,
que deve troca-la no primeiro acesso pela opcao "Alterar Senha" no painel.

---

## Funcionalidades

| Modulo          | Funcionalidade                                             |
|-----------------|------------------------------------------------------------|
| Login           | Autenticacao segura com Django Auth (PBKDF2-SHA256)        |
| Login do Aluno  | Acesso exclusivo do aluno com email e senha temporaria     |
| Troca de Senha  | Aluno altera a propria senha apos o primeiro acesso        |
| Dashboard       | Visao geral com graficos interativos (Chart.js)            |
| Alunos          | Cadastro, edicao, busca e inativacao de alunos             |
| Endereco        | Preenchimento automatico via API ViaCEP                    |
| Treinos         | Criacao de treinos personalizados por aluno                |
| Exercicios      | Banco com 34 exercicios pre-cadastrados por grupo muscular |
| Evolucao Fisica | Registro de peso, altura, IMC e percentual de gordura      |
| Agenda          | Calendario semanal com agendamento de aulas                |
| Painel do Aluno | Aluno visualiza treinos, agenda e evolucao fisica          |
| Pagamentos      | Registro, filtros e controle de pagamentos                 |
| Planos          | Cadastro e edicao de planos com valor e duracao            |
| Alterar Plano   | Troca de plano do aluno com calculo automatico             |
| LGPD            | Aceite de termos registrado no banco com data e hora       |
| Testes          | Suite de testes unitarios com Django TestCase              |

---

## Seguranca implementada

- Senhas criptografadas com **PBKDF2-SHA256** (padrao Django)
- Senha inicial do aluno **gerada aleatoriamente** (10 caracteres)
- Protecao **CSRF** em todos os formularios
- **@login_required** em todas as rotas autenticadas
- Rotas administrativas **bloqueadas para alunos** (verificacao is_staff)
- **X_FRAME_OPTIONS = DENY** contra clickjacking
- Sessao com expiracao automatica em 24 horas
- Credenciais e SECRET_KEY em variaveis de ambiente (.env)

---

## Banco de Dados (SQLite 3)

- `auth_user` — usuarios do sistema
- `alunos_aluno` — dados dos alunos (inclui aceite_lgpd e data_aceite_lgpd)
- `alunos_evolutionfisica` — evolucao fisica
- `treinos_treino` — treinos criados
- `treinos_exercicio` — banco de exercicios
- `treinos_treinoexercicio` — exercicios por treino
- `financeiro_plano` — planos disponiveis
- `financeiro_pagamento` — controle de pagamentos
- `agenda_aula` — agendamento de aulas

Para visualizar o banco recomenda-se o **DB Browser for SQLite**
(abrir `backend/db.sqlite3` em modo somente leitura).

---

## Tecnologias

- Backend: Python 3.11 + Django 4.2 (padrao MTV)
- Frontend: HTML5, CSS3, Bootstrap 5.3, JavaScript
- Banco de Dados: SQLite 3
- Graficos: Chart.js
- API externa: ViaCEP
- Icones: Bootstrap Icons 1.11
- Testes: Django TestCase

---

## LGPD — Lei Geral de Protecao de Dados

O sistema implementa conformidade com a Lei n. 13.709/2018:

- Termos de uso exibidos no login do personal trainer
- Checkbox de aceite obrigatorio no login do aluno
- Data e hora do aceite registrados na tabela alunos_aluno
- Declaracao de responsabilidade no cadastro de alunos
- Pagina de Politica de Privacidade disponivel em /politica-privacidade/

---

## Trabalhos Futuros

- Troca de senha do personal trainer pelo proprio sistema
- Deploy em ambiente de producao (PostgreSQL + Gunicorn + HTTPS)
- Paginacao nas listagens
- Ampliacao da cobertura de testes automatizados
