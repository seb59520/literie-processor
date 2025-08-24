@echo off
chcp 65001 >nul

echo ========================================
echo    MATELASAPP - LANCEMENT PRINCIPAL
echo ========================================
echo.

REM Aller dans le dossier des scripts Windows
cd /d "%~dp0build_scripts\windows"

REM Lancer le menu principal
call "menu_ascii.bat" 