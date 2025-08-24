@echo off
echo ========================================
echo    Installation Simple Matelas
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

echo Lancement de l'installation simplifiee...
python setup_simple.py

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
echo Lancez install.bat pour creer un raccourci
echo.
pause 