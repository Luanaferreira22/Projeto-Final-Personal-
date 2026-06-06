# Personal Manager — Gestao de Treinos para Personal Trainer

**TCC — Sistemas de Informacao | UMC — Luana Ferreira — 2026**

Sistema web para personal trainers gerenciarem alunos, treinos, agenda e controle financeiro.

---

## Como rodar o projeto

### 1. Instalar dependencias

```bash
pip install django==4.2.7 Pillow==10.1.0
```

### 2. Configurar variaveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

### 3. Aplicar as migracoes

```bash
cd backend
python manage.py migrate
```

### 4. Criar o superusuario (personal trainer)

```bash
python create_superuser.py
```

### 5. Iniciar o servidor

```bash
python manage.py runserver
```

### 6. Acessar no navegador

```
http://127.0.0.1:8000/
```

---

## Acessos do sistema

| Tipo            | URL                              |
|-----------------|----------------------------------|
| Personal Trainer| http://127.0.0.1:8000/login/     |
| Aluno           | http://127.0.0.1:8000/aluno/login/ |
| Agenda          | http://127.0.0.1:8000/agenda/    |

> As credenciais de acesso sao configuradas no arquivo `.env` que nao e versionado por seguranca.

---

## Funcionalidades

| Modulo              | Funcionalidade                                          |
|---------------------|---------------------------------------------------------|
| **Login**           | Autenticacao segura com Django Auth (PBKDF2-SHA256)     |
| **Login do Aluno**  | Acesso exclusivo do aluno com email e senha             |
| **Dashboard**       | Visao geral com graficos interativos (Chart.js)         |
| **Alunos**          | Cadastro, edicao, busca e inativacao de alunos          |
| **Endereco**        | Preenchimento automatico via API ViaCEP                 |
| **Treinos**         | Criacao de treinos personalizados por aluno             |
| **Exercicios**      | Banco com 34 exercicios pre-cadastrados por grupo muscular |
| **Evolucao Fisica** | Registro de peso, altura, IMC e percentual de gordura   |
| **Agenda**          | Calendario semanal com agendamento de aulas             |
| **Painel do Aluno** | Aluno visualiza treinos, agenda e evolucao fisica       |
| **Pagamentos**      | Registro, filtros e controle de pagamentos              |
| **Planos**          | Cadastro e edicao de planos com valor e duracao         |
| **Alterar Plano**   | Troca de plano do aluno com calculo automatico          |
| **LGPD**            | Aceite de termos registrado no banco com data e hora    |
| **Seguranca**       | CSRF, @login_required e protecao de credenciais         |

---

## Banco de Dados (SQLite 3)

Tabelas principais:

- `auth_user` — usuarios do sistema
- `alunos_aluno` — dados dos alunos (inclui aceite_lgpd e data_aceite_lgpd)
- `alunos_evolutionfisica` — evolucao fisica
- `treinos_treino` — treinos criados
- `treinos_exercicio` — banco de exercicios
- `treinos_treinoexercicio` — exercicios por treino
- `financeiro_plano` — planos disponiveis
- `financeiro_pagamento` — controle de pagamentos
- `agenda_aula` — agendamento de aulas

---

## Tecnologias

- **Backend:** Python 3.11 + Django 4.2
- **Frontend:** HTML5, CSS3, Bootstrap 5.3, JavaScript
- **Banco de Dados:** SQLite 3
- **Graficos:** Chart.js
- **API externa:** ViaCEP (preenchimento automatico de endereco)
- **Icones:** Bootstrap Icons 1.11
- **Seguranca:** PBKDF2-SHA256, CSRF, LGPD

---

## Estrutura do Projeto

```
gestao_personal/
    backend/
        gestao_personal/    <- configuracoes Django
        alunos/             <- modulo de alunos
        treinos/            <- modulo de treinos
        financeiro/         <- modulo financeiro
        agenda/             <- modulo de agenda
        core/               <- login, dashboard, painel do aluno
        db.sqlite3          <- banco de dados
        manage.py
    
```

---

## LGPD — Lei Geral de Protecao de Dados

O sistema implementa conformidade com a Lei n. 13.709/2018:

- Termos de uso exibidos no login do personal trainer
- Checkbox de aceite obrigatorio no login do aluno
- Data e hora do aceite registrados na tabela `alunos_aluno`
- Declaracao de responsabilidade no cadastro de alunos
- Pagina de Politica de Privacidade disponivel em `/politica-privacidade/`
