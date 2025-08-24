@echo off
echo ========================================
echo    Creation Executable Debug Windows
echo ========================================
echo.

echo Creation d'un executable avec console visible...
python fix_executable_windows.py

if errorlevel 1 (
    echo ERREUR lors de la creation
    pause
    exit /b 1
)

echo.
echo OK: Executable de debug cree !
echo.
echo Pour lancer avec debug:
echo   1. Double-cliquez sur dist\MatelasApp_Debug.exe
echo   2. Ou utilisez launch_with_console.bat
echo.
echo Les erreurs seront visibles dans la console.
echo.
pause 