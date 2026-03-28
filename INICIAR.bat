@echo off
chcp 65001 >nul
title Personal Manager — Setup Automatico

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║       PERSONAL MANAGER — Setup Automático    ║
echo  ║    TCC — Sistemas de Informação — UMC 2026   ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: ─── Verificar se Python está instalado ─────────────────────
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo  [ERRO] Python nao encontrado!
    echo.
    echo  Instale o Python em: https://www.python.org/downloads/
    echo  IMPORTANTE: Marque a opcao "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)

echo  [OK] Python encontrado.

:: ─── Instalar Django ─────────────────────────────────────────
echo.
echo  [1/4] Instalando Django...
pip install django==4.2.7 Pillow==10.1.0 --quiet
IF ERRORLEVEL 1 (
    echo  [ERRO] Falha ao instalar Django. Verifique sua conexao com a internet.
    pause
    exit /b 1
)
echo  [OK] Django instalado.

:: ─── Criar migrações ─────────────────────────────────────────
echo.
echo  [2/4] Criando estrutura do banco de dados...
python manage.py makemigrations alunos treinos financeiro --no-input >nul 2>&1
python manage.py migrate --no-input >nul 2>&1
IF ERRORLEVEL 1 (
    echo  [ERRO] Falha ao criar o banco de dados.
    pause
    exit /b 1
)
echo  [OK] Banco de dados criado (db.sqlite3).

:: ─── Popular dados iniciais ──────────────────────────────────
echo.
echo  [3/4] Inserindo dados iniciais (exercicios, planos, usuario)...
python popular_db.py
IF ERRORLEVEL 1 (
    echo  [AVISO] Erro ao popular dados. O sistema ainda pode funcionar.
)
echo  [OK] Dados inseridos.

:: ─── Abrir no navegador e iniciar servidor ───────────────────
echo.
echo  [4/4] Iniciando o servidor...
echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║  Acesse:  http://127.0.0.1:8000/            ║
echo  ║  Usuario: personal                           ║
echo  ║  Senha:   personal123                        ║
echo  ║                                              ║
echo  ║  Pressione CTRL+C para parar o servidor.     ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: Abre o navegador automaticamente após 2 segundos
start "" timeout /t 2 >nul
start "" "http://127.0.0.1:8000/"

python manage.py runserver

pause
