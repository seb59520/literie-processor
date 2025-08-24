@echo off
echo ========================================
echo    Application Matelas - Lancement Simple
echo ========================================
echo.

echo Lancement de l'application avec Python...
echo (Cette methode fonctionne car debug_windows.bat fonctionne)
echo.

cd /d "%~dp0"
python run_gui.py

echo.
echo Application fermee.
pause 