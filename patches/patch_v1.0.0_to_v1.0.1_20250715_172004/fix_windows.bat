@echo off
echo ========================================
echo    Correction Executable Windows
echo ========================================
echo.

echo Correction de l'executable Windows...
echo (Base sur le fait que debug_windows.bat fonctionne)
echo.

python fix_windows_executable.py

if errorlevel 1 (
    echo.
    echo ERREUR lors de la correction
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Correction Terminee !
echo ========================================
echo.
echo Votre application corrigee se trouve dans: dist\MatelasApp\
echo.
echo Pour lancer l'application:
echo   1. Double-cliquez sur dist\MatelasApp\MatelasApp.exe
echo   2. Ou double-cliquez sur dist\MatelasApp\launch.bat
echo   3. Ou double-cliquez sur dist\MatelasApp\install_shortcut.bat
echo.
echo L'application devrait maintenant fonctionner correctement !
echo.
pause 