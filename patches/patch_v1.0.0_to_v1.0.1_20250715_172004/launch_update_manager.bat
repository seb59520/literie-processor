@echo off
echo ========================================
echo   Gestionnaire de Mises a Jour
echo   Matelas App
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

echo Python detecte, lancement du gestionnaire...
echo.

REM Lancer le gestionnaire de mises à jour
python update_manager_gui.py

if errorlevel 1 (
    echo.
    echo ERREUR: Impossible de lancer le gestionnaire de mises a jour
    echo Verifiez que tous les fichiers sont presents
    pause
    exit /b 1
)

echo.
echo Gestionnaire ferme.
pause 