@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo    LANCEUR APPLICATION MATELASAPP
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo SOLUTION: Installez Python depuis https://python.org
    pause
    exit /b 1
)

echo OK: Python detecte
python --version

REM Vérifier les dépendances PyQt6
echo.
echo Verification des dependances...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo ERREUR: PyQt6 n'est pas installe
    echo Installation de PyQt6...
    pip install PyQt6
    if errorlevel 1 (
        echo ERREUR: Echec de l'installation de PyQt6
        pause
        exit /b 1
    )
)

echo OK: PyQt6 installe

REM Vérifier openpyxl
python -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    echo Installation d'openpyxl...
    pip install openpyxl
    if errorlevel 1 (
        echo ERREUR: Echec de l'installation d'openpyxl
        pause
        exit /b 1
    )
)

echo OK: openpyxl installe

REM Vérifier requests
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installation de requests...
    pip install requests
    if errorlevel 1 (
        echo ERREUR: Echec de l'installation de requests
        pause
        exit /b 1
    )
)

echo OK: requests installe

echo.
echo Lancement de l'application...
echo.

REM Lancer l'application
python app_gui.py
if errorlevel 1 (
    echo.
    echo ERREUR lors du lancement de l'application
    echo.
    echo SOLUTIONS:
    echo 1. Verifiez que tous les fichiers sont presents
    echo 2. Essayez: pip install --upgrade PyQt6
    echo 3. Verifiez les logs d'erreur ci-dessus
    echo.
    pause
    exit /b 1
)

echo.
echo Application fermee normalement
pause 