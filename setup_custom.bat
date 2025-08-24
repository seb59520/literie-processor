@echo off
chcp 65001 >nul
echo ========================================
echo INSTALLATION MATELAS APP - VERSION PERSONNALISEE
echo ========================================
echo.

echo Utilisation de votre commande PyInstaller specifique:
echo C:\Users\SEBASTIEN\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller.exe
echo.

echo Lancement de l'installation...
echo Cette operation peut prendre plusieurs minutes.
echo.

python setup_custom.py

echo.
echo ========================================
echo INSTALLATION TERMINEE
echo ========================================
echo.
echo Si l'installation a reussi:
echo 1. Lancez test_custom.bat pour tester
echo 2. Ou utilisez le package d'installation
echo.
pause 