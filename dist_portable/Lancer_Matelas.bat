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

REM Verifier les dependances avec le script de verification
echo Verification complete des modules...
python check_dependencies.py
if errorlevel 1 (
    echo.
    echo [ATTENTION] Dependances manquantes detectees
    echo L'application peut ne pas fonctionner correctement
    echo.
    pause
)

echo.

REM Lancer l'application
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
    echo 1. ERREUR 401 (API): Executez Test_API.bat
    echo 2. Modules manquants: python check_dependencies.py
    echo 3. Redimensionnement: Test_Resize.bat
    echo 4. Verifiez que Python 3.8+ est installe correctement
    echo 5. Executez ce script en tant qu'administrateur
    echo 6. Consultez GUIDE_API_KEYS.txt pour la configuration
    echo.
    echo Diagnostics rapides:
    echo - Test API: Test_API.bat
    echo - Test modules: python check_dependencies.py
    echo - Test interface: Test_Resize.bat
    echo.
    pause
) else (
    echo.
    echo [OK] Application fermee normalement
)