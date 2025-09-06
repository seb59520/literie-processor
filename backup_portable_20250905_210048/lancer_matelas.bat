@echo off
title MatelasProcessor v3.11.9
echo 🚀 Démarrage de MatelasProcessor v3.11.9
echo 📡 Mise à jour automatique activée
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python 3.8 ou plus récent
    pause
    exit /b 1
)

REM Installer les dépendances si nécessaire
echo 📦 Vérification des dépendances...
python -c "import PyQt6" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 Installation de PyQt6...
    pip install PyQt6
)

REM Lancer l'application
echo ▶️ Lancement de l'application...
python app_gui.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Erreur lors du lancement
    pause
)
