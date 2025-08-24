@echo off
chcp 65001 >nul
echo 🚀 Lancement de l'application de test LLM...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non trouvé dans le PATH
    echo 💡 Installez Python depuis https://python.org
    pause
    exit /b 1
)

REM Lancer l'application
python lancer_test_llm.py

if errorlevel 1 (
    echo.
    echo ❌ Erreur lors du lancement
    pause
) 