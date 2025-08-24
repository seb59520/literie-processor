@echo off
chcp 65001 >nul

echo ========================================
echo    DIAGNOSTIC COMPLET MATELASAPP
echo ========================================
echo.

REM Aller dans le dossier racine
cd /d "%~dp0..\.."
echo Dossier: %CD%
echo.

echo [1/6] Diagnostic Python...
python --version
if errorlevel 1 (
    echo ERREUR: Python non trouve
    echo    Installez Python depuis python.org
) else (
    echo Python trouve
)
echo.

echo [2/6] Diagnostic dependances...
python -c "import PyQt6; print('PyQt6 trouve')" 2>nul
if errorlevel 1 (
    echo ERREUR: PyQt6 non trouve
    echo    Installez avec: pip install PyQt6
) else (
    echo PyQt6 trouve
)

python -c "import openpyxl; print('openpyxl trouve')" 2>nul
if errorlevel 1 (
    echo ERREUR: openpyxl non trouve
    echo    Installez avec: pip install openpyxl
) else (
    echo openpyxl trouve
)

python -c "import requests; print('requests trouve')" 2>nul
if errorlevel 1 (
    echo ERREUR: requests non trouve
    echo    Installez avec: pip install requests
) else (
    echo requests trouve
)

python -c "import PyInstaller; print('PyInstaller trouve')" 2>nul
if errorlevel 1 (
    echo ERREUR: PyInstaller non trouve
    echo    Installez avec: pip install pyinstaller
) else (
    echo PyInstaller trouve
)
echo.

echo [3/6] Diagnostic fichiers de configuration...
if exist "config\mappings_matelas.json" (
    echo mappings_matelas.json trouve
) else (
    echo ERREUR: mappings_matelas.json manquant
)

if exist "config\mappings_sommiers.json" (
    echo mappings_sommiers.json trouve
) else (
    echo ERREUR: mappings_sommiers.json manquant
)

if exist "requirements_gui.txt" (
    echo requirements_gui.txt trouve
) else (
    echo ERREUR: requirements_gui.txt manquant
)
echo.

echo [4/6] Diagnostic ressources principales...
if exist "app_gui.py" (
    echo app_gui.py trouve
) else (
    echo ERREUR: app_gui.py manquant
)

if exist "backend\" (
    echo Dossier backend trouve
) else (
    echo ERREUR: Dossier backend manquant
)

if exist "backend\Referentiels\" (
    echo Dossier Referentiels trouve
) else (
    echo ERREUR: Dossier Referentiels manquant
)

if exist "assets\" (
    echo Dossier assets trouve
) else (
    echo ERREUR: Dossier assets manquant
)

if exist "template\" (
    echo Dossier template trouve
) else (
    echo ERREUR: Dossier template manquant
)
echo.

echo [5/6] Test des mappings...
echo Test du chargement des mappings...
python test_mappings_production.py
echo.

echo [6/6] Diagnostic executable...
if exist "dist\MatelasApp.exe" (
    echo Executable trouve: dist\MatelasApp.exe
    for %%A in ("dist\MatelasApp.exe") do (
        echo    Taille: %%~zA octets
    )
    echo.
    echo Test de l'executable...
    echo Voulez-vous tester l'executable? (o/n)
    set /p test_exe="Votre choix: "
    if /i "%test_exe%"=="o" (
        echo Lancement de l'executable pour test...
        start "" "dist\MatelasApp.exe"
        echo Executable lance!
    ) else if /i "%test_exe%"=="oui" (
        echo Lancement de l'executable pour test...
        start "" "dist\MatelasApp.exe"
        echo Executable lance!
    )
) else (
    echo ERREUR: Executable non trouve
    echo    Compilez d'abord avec l'installation
)
echo.

echo ========================================
echo    DIAGNOSTIC TERMINE
echo ========================================
echo.
echo Resume:
echo    - Si des erreurs sont detectees, lancez l'installation
echo    - Si tout est OK, vous pouvez lancer l'application
echo.
echo Actions recommandees:
echo    1. Si des erreurs: lancez install_ascii.bat
echo    2. Si tout OK: lancez lancer_ascii.bat
echo.
pause 