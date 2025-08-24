@echo off
chcp 65001 >nul
echo 🔨 ADMIN BUILDER - LANCEUR RAPIDE
echo ==================================
echo.

REM Vérifier que nous sommes dans le bon répertoire
if not exist "admin_builder_gui.py" (
    echo ❌ Erreur: admin_builder_gui.py non trouvé
    echo    Assurez-vous d'être dans le répertoire MATELAS_FINAL
    pause
    exit /b 1
)

echo ✅ Répertoire correct détecté
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Erreur: Python non trouvé
    echo    Installez Python avant de continuer
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.

REM Lancer l'Admin Builder
echo 🚀 Lancement de l'Admin Builder...
echo    Interface graphique en cours d'ouverture...
echo.

python admin_builder_gui.py

echo.
echo ✅ Admin Builder fermé
pause 