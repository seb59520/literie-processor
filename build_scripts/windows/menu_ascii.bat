@echo off
chcp 65001 >nul

:menu
cls
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
set /p choice="Votre choix (1-6): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto launch
if "%choice%"=="3" goto diagnostic
if "%choice%"=="4" goto clean
if "%choice%"=="5" goto info
if "%choice%"=="6" goto end
echo Choix invalide. Veuillez reessayer.
timeout /t 2 >nul
goto menu

:install
echo.
echo ========================================
echo    INSTALLATION COMPLETE
echo ========================================
echo.
echo Lancement de l'installation...
echo.
call "%~dp0\install_ascii.bat"
echo.
echo Appuyez sur une touche pour revenir au menu...
pause >nul
goto menu

:launch
echo.
echo ========================================
echo    LANCEMENT DE L'APPLICATION
echo ========================================
echo.
echo Lancement de l'application...
echo.
call "%~dp0\lancer_ascii.bat"
echo.
echo Appuyez sur une touche pour revenir au menu...
pause >nul
goto menu

:diagnostic
echo.
echo ========================================
echo    DIAGNOSTIC COMPLET
echo ========================================
echo.
echo Lancement du diagnostic...
echo.
call "%~dp0\diagnostic_ascii.bat"
echo.
echo Appuyez sur une touche pour revenir au menu...
pause >nul
goto menu

:clean
echo.
echo ========================================
echo    NETTOYAGE DES BUILDS
echo ========================================
echo.
echo Nettoyage en cours...

REM Aller dans le dossier racine
cd /d "%~dp0..\.."

REM Supprimer les dossiers de build
if exist "build" (
    rmdir /s /q "build"
    echo Dossier build supprime
)
if exist "dist" (
    rmdir /s /q "dist"
    echo Dossier dist supprime
)

REM Supprimer les fichiers .spec
for %%f in (*.spec) do (
    del "%%f"
    echo Fichier %%f supprime
)

echo.
echo Nettoyage termine
echo.
echo Appuyez sur une touche pour revenir au menu...
pause >nul
goto menu

:info
echo.
echo ========================================
echo    INFORMATIONS MATELASAPP
echo ========================================
echo.
echo MatelasApp - Processeur de Literie
echo.
echo Fonctionnalites:
echo    - Traitement automatique des commandes PDF
echo    - Generation d'Excel avec mappings
echo    - Interface graphique moderne
echo    - Support des matelas et sommiers
echo.
echo Prerequis:
echo    - Windows 10/11
echo    - Python 3.8+ (pour l'installation)
echo    - 100 MB d'espace disque
echo.
echo Structure:
echo    - app_gui.py: Interface principale
echo    - backend/: Logique metier
echo    - config/: Fichiers de configuration
echo    - assets/: Images et icones
echo    - template/: Templates Excel
echo.
echo Utilisation:
echo    1. Installation: Option [1]
echo    2. Lancement: Option [2]
echo    3. Diagnostic: Option [3]
echo.
echo Support:
echo    - Verifiez les logs en cas de probleme
echo    - Utilisez le diagnostic pour identifier les erreurs
echo.
echo Appuyez sur une touche pour revenir au menu...
pause >nul
goto menu

:end
echo.
echo Au revoir!
timeout /t 2 >nul
exit 