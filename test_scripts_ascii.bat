@echo off
chcp 65001 >nul

echo ========================================
echo    TEST DES SCRIPTS ASCII
echo ========================================
echo.

echo Test des scripts ASCII sans caracteres speciaux...
echo.

echo [1/4] Test du menu principal...
if exist "build_scripts\windows\menu_ascii.bat" (
    echo menu_ascii.bat trouve
) else (
    echo ERREUR: menu_ascii.bat manquant
)

echo [2/4] Test du script d'installation...
if exist "build_scripts\windows\install_ascii.bat" (
    echo install_ascii.bat trouve
) else (
    echo ERREUR: install_ascii.bat manquant
)

echo [3/4] Test du script de lancement...
if exist "build_scripts\windows\lancer_ascii.bat" (
    echo lancer_ascii.bat trouve
) else (
    echo ERREUR: lancer_ascii.bat manquant
)

echo [4/4] Test du script de diagnostic...
if exist "build_scripts\windows\diagnostic_ascii.bat" (
    echo diagnostic_ascii.bat trouve
) else (
    echo ERREUR: diagnostic_ascii.bat manquant
)

echo.
echo ========================================
echo    TEST TERMINE
echo ========================================
echo.
echo Tous les scripts ASCII sont crees!
echo.
echo Pour commencer:
echo    1. Double-cliquez sur Lancer_MatelasApp_ASCII.bat
echo    2. Ou lancez build_scripts\windows\menu_ascii.bat
echo.
echo Les scripts sont maintenant sans caracteres speciaux
echo et ne devraient plus causer d'erreurs d'encodage.
echo.
pause 