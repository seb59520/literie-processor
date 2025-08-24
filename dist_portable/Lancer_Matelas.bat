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
    echo.
    echo Veuillez installer Python 3.8+ depuis:
    echo https://python.org/downloads/
    echo.
    echo IMPORTANT: Cochez "Add Python to PATH" pendant l'installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

REM Changer vers le dossier du script
cd /d "%~dp0"

REM Installer les dependances
echo Installation des dependances necessaires...
echo Ceci peut prendre quelques minutes la premiere fois...
echo.

python -m pip install --upgrade pip --quiet --disable-pip-version-check 2>nul
python -m pip install PyQt6 --quiet --disable-pip-version-check 2>nul
python -m pip install requests --quiet --disable-pip-version-check 2>nul
python -m pip install pandas --quiet --disable-pip-version-check 2>nul
python -m pip install openpyxl --quiet --disable-pip-version-check 2>nul
python -m pip install psutil --quiet --disable-pip-version-check 2>nul

echo [OK] Dependencies installees
echo.

REM Verifier que les modules critiques sont disponibles
echo Verification des modules...
python -c "import PyQt6.QtWidgets; print('[OK] PyQt6 disponible')" 2>nul
if errorlevel 1 (
    echo [ERREUR] PyQt6 non disponible
    echo Reinstallation de PyQt6...
    python -m pip install PyQt6 --force-reinstall --quiet
)

REM Lancer l'application
echo.
echo Lancement du Processeur de Devis Literie...
echo.

python app_gui.py

REM Gestion des erreurs
if errorlevel 1 (
    echo.
    echo ================================================================
    echo [ERREUR] L'application a rencontre une erreur
    echo ================================================================
    echo.
    echo Solutions possibles:
    echo 1. Verifiez que Python 3.8+ est installe
    echo 2. Executez ce script en tant qu'administrateur
    echo 3. Verifiez votre connexion internet (pour les API)
    echo 4. Consultez le fichier README_PORTABLE.txt
    echo.
    echo Pour obtenir de l'aide, contactez le support technique
    echo.
    pause
) else (
    echo.
    echo [OK] Application fermee normalement
)