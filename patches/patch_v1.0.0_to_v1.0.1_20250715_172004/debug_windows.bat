@echo off
echo ========================================
echo    Diagnostic Application Matelas
echo ========================================
echo.

echo 1. Verification de l'environnement...
echo.

echo Python version:
python --version
if errorlevel 1 (
    echo ERREUR: Python non trouve
    pause
    exit /b 1
)

echo.
echo 2. Verification des fichiers...
echo.

if exist "dist\MatelasApp\MatelasApp.exe" (
    echo OK: Executable trouve
    echo Chemin: %CD%\dist\MatelasApp\MatelasApp.exe
) else (
    echo ERREUR: Executable non trouve
    echo Cherchez dans: dist\MatelasApp\
    pause
    exit /b 1
)

echo.
echo 3. Test de lancement avec console...
echo.

echo Lancement de l'application avec affichage des erreurs...
cd dist\MatelasApp
MatelasApp.exe --debug
if errorlevel 1 (
    echo ERREUR lors du lancement
    echo.
    echo 4. Verification des logs...
    if exist "logs\matelas_errors.log" (
        echo Dernieres erreurs:
        type logs\matelas_errors.log
    ) else (
        echo Aucun fichier de log d'erreur trouve
    )
) else (
    echo Application lancee avec succes
)

echo.
echo 5. Test de lancement direct Python...
echo.

cd ..\..
echo Test avec Python direct:
python run_gui.py
if errorlevel 1 (
    echo ERREUR avec Python direct
) else (
    echo OK: Python direct fonctionne
)

echo.
echo Diagnostic termine.
pause 