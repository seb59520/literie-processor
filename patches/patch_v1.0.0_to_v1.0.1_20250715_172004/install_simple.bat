@echo off
echo ========================================
echo    Installation Application Matelas
echo ========================================
echo.

echo Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo.
    echo Veuillez installer Python 3.8+ depuis:
    echo https://www.python.org/downloads/
    echo.
    echo Assurez-vous de cocher "Add Python to PATH" lors de l'installation
    pause
    exit /b 1
)

echo OK: Python detecte
echo.

echo Lancement de l'installation automatique...
python setup_windows.py

if errorlevel 1 (
    echo.
    echo ERREUR lors de l'installation
    pause
    exit /b 1
)

echo.
echo Installation terminee avec succes !
echo.
echo Votre application se trouve dans: dist\MatelasApp\
echo Pour installer sur un autre PC:
echo    1. Copiez le dossier dist\MatelasApp\
echo    2. Lancez install.bat pour creer un raccourci
echo    3. Ou lancez directement MatelasApp.exe
echo.
pause 