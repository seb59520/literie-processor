@echo off
echo ========================================
echo    Creation Executable Debug
echo ========================================
echo.

echo Creation de l'executable avec console...
python setup_debug.py

if errorlevel 1 (
    echo.
    echo ERREUR lors de la creation
    pause
    exit /b 1
)

echo.
echo Executable debug cree !
echo Lancez: dist\MatelasApp_Debug.exe
echo Vous verrez les erreurs dans la console
echo.
pause 