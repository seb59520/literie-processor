@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo    🚀 LANCEUR APPLICATION MATELASAPP
echo ========================================
echo.

:: Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo 💡 Installez Python depuis https://python.org
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version

:: Vérifier les dépendances PyQt6
echo.
echo 🔍 Vérification des dépendances...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo ❌ PyQt6 n'est pas installé
    echo 📦 Installation de PyQt6...
    pip install PyQt6
    if errorlevel 1 (
        echo ❌ Échec de l'installation de PyQt6
        pause
        exit /b 1
    )
)

echo ✅ PyQt6 installé

:: Vérifier les autres dépendances
python -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installation d'openpyxl...
    pip install openpyxl
)

python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installation de requests...
    pip install requests
)

echo ✅ Toutes les dépendances sont installées

:: Lancer l'application
echo.
echo 🚀 Lancement de l'application MatelasApp...
echo.

python app_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Erreur lors du lancement de l'application
    echo.
    echo 🔧 Solutions possibles :
    echo 1. Vérifiez que PyQt6 est correctement installé
    echo 2. Essayez : pip install --upgrade PyQt6
    echo 3. Vérifiez les logs d'erreur ci-dessus
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Application fermée normalement
pause 