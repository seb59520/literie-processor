@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo    🔍 DIAGNOSTIC PYQT6 WINDOWS
echo ========================================
echo.

:: Informations système
echo 📋 Informations système :
echo.
echo Version Windows :
ver
echo.

echo Architecture :
echo %PROCESSOR_ARCHITECTURE%
echo.

:: Vérifier Python
echo 🔍 Vérification Python :
python --version 2>nul
if errorlevel 1 (
    echo ❌ Python non trouvé
    goto :end
)

echo ✅ Python trouvé
echo.

:: Vérifier pip
echo 🔍 Vérification pip :
pip --version 2>nul
if errorlevel 1 (
    echo ❌ pip non trouvé
    goto :end
)

echo ✅ pip trouvé
echo.

:: Vérifier PyQt6
echo 🔍 Vérification PyQt6 :
python -c "import PyQt6; print('✅ PyQt6 version:', PyQt6.QtCore.PYQT_VERSION_STR)" 2>nul
if errorlevel 1 (
    echo ❌ PyQt6 non installé ou erreur d'import
    echo.
    echo 📦 Tentative d'installation de PyQt6...
    pip install PyQt6
    echo.
    echo 🔍 Nouvelle vérification :
    python -c "import PyQt6; print('✅ PyQt6 version:', PyQt6.QtCore.PYQT_VERSION_STR)" 2>nul
    if errorlevel 1 (
        echo ❌ Échec de l'installation/import de PyQt6
        goto :end
    )
)

echo.

:: Vérifier les modules PyQt6 spécifiques
echo 🔍 Vérification des modules PyQt6 :
echo.

echo - QtWidgets :
python -c "from PyQt6.QtWidgets import QApplication; print('✅ QtWidgets OK')" 2>nul
if errorlevel 1 (
    echo ❌ Erreur QtWidgets
    echo.
    echo 🔧 Tentative de réparation :
    pip uninstall PyQt6 -y
    pip install PyQt6
    echo.
    python -c "from PyQt6.QtWidgets import QApplication; print('✅ QtWidgets OK après réparation')" 2>nul
    if errorlevel 1 (
        echo ❌ Échec de la réparation
    )
)

echo - QtCore :
python -c "from PyQt6.QtCore import QThread; print('✅ QtCore OK')" 2>nul
if errorlevel 1 echo ❌ Erreur QtCore

echo - QtGui :
python -c "from PyQt6.QtGui import QIcon; print('✅ QtGui OK')" 2>nul
if errorlevel 1 echo ❌ Erreur QtGui

echo.

:: Test d'import de l'application
echo 🔍 Test d'import de l'application :
python -c "from app_gui import MatelasApp; print('✅ Import app_gui OK')" 2>nul
if errorlevel 1 (
    echo ❌ Erreur d'import app_gui
    echo.
    echo 🔍 Détail de l'erreur :
    python -c "from app_gui import MatelasApp" 2>&1
)

echo.

:: Vérifier les dépendances
echo 🔍 Vérification des autres dépendances :
echo.

python -c "import openpyxl; print('✅ openpyxl OK')" 2>nul
if errorlevel 1 echo ❌ openpyxl manquant

python -c "import requests; print('✅ requests OK')" 2>nul
if errorlevel 1 echo ❌ requests manquant

python -c "import json; print('✅ json OK')" 2>nul
if errorlevel 1 echo ❌ json manquant

echo.

:: Recommandations
echo 📋 Recommandations :
echo.
echo 1. Si PyQt6 pose problème, essayez :
echo    pip uninstall PyQt6 -y
echo    pip install PyQt6==6.5.0
echo.
echo 2. Si l'erreur persiste, essayez :
echo    pip install PySide6
echo    (et modifiez les imports dans app_gui.py)
echo.
echo 3. Vérifiez que vous utilisez Python 3.8+
echo.

:end
echo.
echo ========================================
echo    FIN DU DIAGNOSTIC
echo ========================================
pause 