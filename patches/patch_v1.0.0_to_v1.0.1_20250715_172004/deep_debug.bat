@echo off
chcp 65001 >nul
echo ========================================
echo DIAGNOSTIC APPROFONDI - MATELAS APP
echo ========================================
echo.

echo Lancement du diagnostic approfondi...
echo.

python deep_debug.py

echo.
echo ========================================
echo DIAGNOSTIC TERMINE
echo ========================================
echo.
echo Si des erreurs sont detectees, verifiez:
echo 1. L'executable minimal: dist\MatelasApp_Minimal.exe
echo 2. Les fichiers de test crees
echo 3. Les logs d'erreur
echo.
pause 