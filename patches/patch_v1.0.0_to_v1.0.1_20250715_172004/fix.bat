@echo off
echo ========================================
echo    Reparation Executable Matelas
echo ========================================
echo.

echo Lancement de la reparation...
python fix_executable.py

if errorlevel 1 (
    echo.
    echo ERREUR lors de la reparation
    pause
    exit /b 1
)

echo.
echo Reparation terminee avec succes !
echo.
echo Votre application corrigee se trouve dans: dist\MatelasApp_Fixed\
echo Lancez install.bat pour creer un raccourci
echo.
pause 