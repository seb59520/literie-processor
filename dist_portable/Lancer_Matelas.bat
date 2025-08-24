@echo off
echo ========================================
echo    Processeur de Devis Literie
echo           Version Portable
echo ========================================
echo.

REM Verifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe
    echo Veuillez installer Python 3.8+ depuis python.org
    echo Appuyez sur une touche pour continuer...
    pause >nul
    exit /b 1
)

REM Installer les dependances si necessaire
echo Installation des dependances...
pip install PyQt6 requests pandas openpyxl psutil --quiet --disable-pip-version-check

REM Lancer l'application
echo.
echo Lancement de l'application...
python app_gui.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Erreur lors du lancement
    echo Appuyez sur une touche pour continuer...
    pause >nul
)