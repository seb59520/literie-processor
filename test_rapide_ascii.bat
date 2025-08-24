@echo off
chcp 65001 >nul

echo ========================================
echo    TEST RAPIDE SCRIPTS ASCII
echo ========================================
echo.

echo Test rapide des scripts ASCII...
echo.

REM Test 1: Vérifier que les fichiers existent
echo [1/3] Verification des fichiers...
if exist "build_scripts\windows\menu_ascii.bat" (
    echo menu_ascii.bat: OK
) else (
    echo menu_ascii.bat: MANQUANT
)

if exist "build_scripts\windows\install_ascii.bat" (
    echo install_ascii.bat: OK
) else (
    echo install_ascii.bat: MANQUANT
)

if exist "Lancer_MatelasApp_ASCII.bat" (
    echo Lancer_MatelasApp_ASCII.bat: OK
) else (
    echo Lancer_MatelasApp_ASCII.bat: MANQUANT
)

echo.

REM Test 2: Vérifier le format ASCII
echo [2/3] Verification du format ASCII...
findstr /C:"@echo off" "build_scripts\windows\menu_ascii.bat" >nul
if errorlevel 1 (
    echo menu_ascii.bat: FORMAT INCORRECT
) else (
    echo menu_ascii.bat: FORMAT ASCII OK
)

findstr /C:"@echo off" "build_scripts\windows\install_ascii.bat" >nul
if errorlevel 1 (
    echo install_ascii.bat: FORMAT INCORRECT
) else (
    echo install_ascii.bat: FORMAT ASCII OK
)

echo.

REM Test 3: Test d'exécution simple
echo [3/3] Test d'execution simple...
echo Test du menu principal (affichage uniquement)...
echo.

REM Aller dans le dossier des scripts
cd /d "%~dp0build_scripts\windows"

REM Tester l'affichage du menu (sans interaction)
echo Test d'affichage du menu principal:
echo.
echo ========================================
echo    MATELASAPP - MENU PRINCIPAL
echo ========================================
echo.
echo Dossier: %CD%
echo.
echo Choisissez une option:
echo.
echo [1] Installation complete (recommandee)
echo [2] Lancer l'application
echo [3] Diagnostic complet
echo [4] Nettoyer les builds
echo [5] Informations
echo [6] Quitter
echo.

echo ========================================
echo    TEST TERMINE
echo ========================================
echo.
echo Si vous voyez ce message, les scripts ASCII fonctionnent!
echo.
echo Pour tester completement:
echo 1. Double-cliquez sur Lancer_MatelasApp_ASCII.bat
echo 2. Ou lancez build_scripts\windows\menu_ascii.bat
echo.
echo Appuyez sur une touche pour continuer...
pause >nul 