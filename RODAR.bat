@echo off
chcp 65001 >nul
title Personal Manager — Servidor

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║         PERSONAL MANAGER — Servidor          ║
echo  ╚══════════════════════════════════════════════╝
echo.
echo  Acesse:  http://127.0.0.1:8000/
echo  Usuario: personal
echo  Senha:   personal123
echo.
echo  Pressione CTRL+C para parar o servidor.
echo.

start "" "http://127.0.0.1:8000/"
python manage.py runserver

pause
