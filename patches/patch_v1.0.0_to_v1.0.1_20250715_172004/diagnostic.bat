@echo off
echo ========================================
echo    Diagnostic Installation Matelas
echo ========================================
echo.

echo Lancement du diagnostic complet...
python diagnostic_installation.py

if errorlevel 1 (
    echo.
    echo ERREUR: Diagnostic echoue
    pause
    exit /b 1
)

echo.
echo Diagnostic termine !
pause 