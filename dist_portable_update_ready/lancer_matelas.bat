@echo off
title MATELAS Application v3.11.12
echo.
echo ================================================
echo    MATELAS Application v3.11.12 - Lancement
echo ================================================
echo.

cd /d "%~dp0"

:: Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python non trouve
    echo.
    echo SOLUTIONS:
    echo    1. Installer Python depuis https://python.org/downloads
    echo    2. Cocher "Add Python to PATH" lors de l'installation
    echo    3. Redemarrer l'invite de commande
    echo    4. Relancer ce script
    echo.
    pause
    exit /b 1
)

echo [OK] Python detecte
python --version
echo.

:: Verifier les dependances
echo Verification des dependances...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Dependances manquantes
    echo.
    echo Executez d'abord: python install.py
    echo.
    pause
    exit /b 1
)

echo [OK] Dependances OK
echo.
echo Lancement de l'application...
echo.

:: Lancer l'application
python app_gui.py

:: Gerer les erreurs
if errorlevel 1 (
    echo.
    echo [ERREUR] Erreur de lancement
    echo.
    echo SOLUTIONS:
    echo    1. Verifier que vous etes dans le bon repertoire
    echo    2. Executer: python install.py
    echo    3. Consulter les logs dans le dossier logs/
    echo.
    echo Fichiers de log utiles:
    if exist logs\app.log echo    - logs\app.log
    if exist logs\errors.log echo    - logs\errors.log
    echo.
)

pause
