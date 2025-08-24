@echo off
echo ========================================
echo    Test Installation Matelas
echo ========================================
echo.

echo Lancement des tests...
python test_installation.py

if errorlevel 1 (
    echo.
    echo ERREUR: Tests echoues
    pause
    exit /b 1
)

echo.
echo Tests termines avec succes !
pause 