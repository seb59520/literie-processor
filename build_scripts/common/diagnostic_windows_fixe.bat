@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo    DIAGNOSTIC WINDOWS MATELASAPP
echo ========================================
echo.

REM Informations systeme
echo Informations systeme:
echo.
echo Version Windows:
ver
echo.

echo Architecture:
echo %PROCESSOR_ARCHITECTURE%
echo.

REM Verification Python
echo Verification Python:
python --version 2>nul
if errorlevel 1 (
    echo ERREUR: Python non trouve
    goto :end
)

echo OK: Python trouve
echo.

REM Verification pip
echo Verification pip:
pip --version 2>nul
if errorlevel 1 (
    echo ERREUR: pip non trouve
    goto :end
)

echo OK: pip trouve
echo.

REM Verification PyQt6
echo Verification PyQt6:
python -c "import PyQt6; print('OK: PyQt6 version:', PyQt6.QtCore.PYQT_VERSION_STR)" 2>nul
if errorlevel 1 (
    echo ERREUR: PyQt6 non installe
    echo Installation...
    pip install PyQt6
    if errorlevel 1 (
        echo ERREUR: Echec de l'installation de PyQt6
        goto :end
    )
    echo OK: PyQt6 installe
) else (
    echo OK: PyQt6 fonctionne
)
echo.

REM Verification openpyxl
echo Verification openpyxl:
python -c "import openpyxl; print('OK: openpyxl version:', openpyxl.__version__)" 2>nul
if errorlevel 1 (
    echo ERREUR: openpyxl non installe
    echo Installation...
    pip install openpyxl
    if errorlevel 1 (
        echo ERREUR: Echec de l'installation d'openpyxl
        goto :end
    )
    echo OK: openpyxl installe
) else (
    echo OK: openpyxl fonctionne
)
echo.

REM Verification requests
echo Verification requests:
python -c "import requests; print('OK: requests version:', requests.__version__)" 2>nul
if errorlevel 1 (
    echo ERREUR: requests non installe
    echo Installation...
    pip install requests
    if errorlevel 1 (
        echo ERREUR: Echec de l'installation de requests
        goto :end
    )
    echo OK: requests installe
) else (
    echo OK: requests fonctionne
)
echo.

REM Verification PyInstaller
echo Verification PyInstaller:
python -c "import PyInstaller; print('OK: PyInstaller disponible')" 2>nul
if errorlevel 1 (
    echo ERREUR: PyInstaller non installe
    echo Installation...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERREUR: Echec de l'installation de PyInstaller
        goto :end
    )
    echo OK: PyInstaller installe
) else (
    echo OK: PyInstaller fonctionne
)
echo.

REM Test d'import de l'application
echo Test d'import de l'application:
python -c "import app_gui; print('OK: app_gui importe avec succes')" 2>nul
if errorlevel 1 (
    echo ERREUR: Impossible d'importer app_gui
    echo.
    echo Diagnostics supplementaires:
    echo 1. Verifiez que app_gui.py existe dans le dossier courant
    echo 2. Verifiez les imports dans app_gui.py
    echo 3. Essayez: pip install --upgrade PyQt6
    goto :end
)

echo OK: Application peut etre importee
echo.

REM Verification des dossiers requis
echo Verification des dossiers requis:
if exist "backend" (
    echo OK: Dossier backend trouve
) else (
    echo ERREUR: Dossier backend manquant
)

if exist "backend\Referentiels" (
    echo OK: Dossier backend\Referentiels trouve
) else (
    echo ERREUR: Dossier backend\Referentiels manquant
)

if exist "config" (
    echo OK: Dossier config trouve
) else (
    echo ERREUR: Dossier config manquant
)

if exist "assets" (
    echo OK: Dossier assets trouve
) else (
    echo ERREUR: Dossier assets manquant
)
echo.

echo ========================================
echo DIAGNOSTIC TERMINE
echo ========================================
echo.
echo Si tous les tests sont OK, l'application devrait fonctionner
echo Si des erreurs apparaissent, suivez les instructions ci-dessus
echo.

:end
pause 