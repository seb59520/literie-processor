@echo off
chcp 65001 >nul
echo ========================================
echo REPARATION AUTOMATIQUE - MATELAS APP
echo ========================================
echo.

echo Lancement de la reparation automatique...
echo Cette operation peut prendre plusieurs minutes.
echo.

python auto_fix.py

echo.
echo ========================================
echo REPARATION TERMINEE
echo ========================================
echo.
echo Si la reparation a reussi:
echo 1. Lancez test_launcher.bat pour tester
echo 2. Ou utilisez le package d'installation
echo.
pause 