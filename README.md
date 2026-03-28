# 🏋️ Personal Manager — Gestão de Treinos para Personal Trainer

**TCC — Sistemas de Informação | UMC — Luana Ferreira — 2026**

Sistema web para personal trainers gerenciarem alunos, treinos e controle financeiro.

---

## 🚀 Como rodar o projeto

### 1. Instalar dependências
```bash
pip install django==4.2.7 Pillow==10.1.0
```

### 2. Aplicar as migrações (cria o banco SQLite)
```bash
python manage.py makemigrations alunos treinos financeiro
python manage.py migrate
```

### 3. Popular dados iniciais (exercícios + planos + login)
```bash
python popular_db.py
```

### 4. Iniciar o servidor
```bash
python manage.py runserver
```

### 5. Acessar no navegador
```
http://127.0.0.1:8000/
```

---

## 🔐 Credenciais padrão

| Campo    | Valor         |
|----------|---------------|
| Usuário  | `personal`    |
| Senha    | `personal123` |

---

## 📋 Funcionalidades

| Módulo         | Funcionalidade                                  |
|----------------|-------------------------------------------------|
| **Login**      | Autenticação segura com Django Auth             |
| **Dashboard**  | Visão geral com gráficos (Chart.js)             |
| **Alunos**     | Cadastro, edição, busca, inativação             |
| **Endereço**   | Preenchimento automático via API ViaCEP         |
| **Treinos**    | Criação, adição/remoção de exercícios           |
| **Exercícios** | Banco com 34 exercícios pré-cadastrados         |
| **Evolução**   | Registro de peso, altura, IMC e % de gordura   |
| **Pagamentos** | Registro, filtros, marcar como pago             |
| **Planos**     | Cadastro e edição de planos com valor/duração   |

---

## 🗄️ Banco de Dados (SQLite)

Tabelas principais:
- `alunos_aluno` — dados dos alunos
- `alunos_evolutionfisica` — evolução física
- `treinos_treino` — treinos criados
- `treinos_exercicio` — banco de exercícios
- `treinos_treinoexercicio` — exercícios por treino
- `financeiro_plano` — planos disponíveis
- `financeiro_pagamento` — controle de pagamentos

---

## 🛠️ Tecnologias

- **Backend:** Python 3 + Django 4.2
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Banco de Dados:** SQLite3
- **Gráficos:** Chart.js
- **API externa:** ViaCEP (preenchimento de endereço)
- **Ícones:** Bootstrap Icons

---

## 📁 Estrutura do Projeto

```
gestao_personal/
├── manage.py
├── popular_db.py          ← Script de dados iniciais
├── requirements.txt
├── gestao_personal/       ← Configurações Django
│   ├── settings.py
│   └── urls.py
├── core/                  ← Login + Dashboard
├── alunos/                ← Gestão de alunos
├── treinos/               ← Gestão de treinos
└── financeiro/            ← Controle financeiro
```
