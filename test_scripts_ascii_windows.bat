@echo off
chcp 65001 >nul

echo ========================================
echo    TEST DES SCRIPTS ASCII WINDOWS
echo ========================================
echo.

echo Test des scripts ASCII sans caracteres speciaux...
echo.

echo [1/5] Test du menu principal...
if exist "build_scripts\windows\menu_ascii.bat" (
    echo menu_ascii.bat trouve
) else (
    echo ERREUR: menu_ascii.bat manquant
)

echo [2/5] Test du script d'installation...
if exist "build_scripts\windows\install_ascii.bat" (
    echo install_ascii.bat trouve
) else (
    echo ERREUR: install_ascii.bat manquant
)

echo [3/5] Test du script de lancement...
if exist "build_scripts\windows\lancer_ascii.bat" (
    echo lancer_ascii.bat trouve
) else (
    echo ERREUR: lancer_ascii.bat manquant
)

echo [4/5] Test du script de diagnostic...
if exist "build_scripts\windows\diagnostic_ascii.bat" (
    echo diagnostic_ascii.bat trouve
) else (
    echo ERREUR: diagnostic_ascii.bat manquant
)

echo [5/5] Test du script de lancement principal...
if exist "Lancer_MatelasApp_ASCII.bat" (
    echo Lancer_MatelasApp_ASCII.bat trouve
) else (
    echo ERREUR: Lancer_MatelasApp_ASCII.bat manquant
)

echo.
echo ========================================
echo    VERIFICATION DU CONTENU
echo ========================================
echo.

echo Test du contenu du menu principal...
findstr /C:"@echo off" "build_scripts\windows\menu_ascii.bat" >nul
if errorlevel 1 (
    echo ERREUR: menu_ascii.bat ne commence pas par @echo off
) else (
    echo menu_ascii.bat: format correct
)

echo Test du contenu du script d'installation...
findstr /C:"@echo off" "build_scripts\windows\install_ascii.bat" >nul
if errorlevel 1 (
    echo ERREUR: install_ascii.bat ne commence pas par @echo off
) else (
    echo install_ascii.bat: format correct
)

echo.
echo ========================================
echo    INSTRUCTIONS DE TEST
echo ========================================
echo.
echo Pour tester les scripts ASCII:
echo.
echo 1. Double-cliquez sur Lancer_MatelasApp_ASCII.bat
echo 2. Ou naviguez vers build_scripts\windows\ et lancez menu_ascii.bat
echo 3. Choisissez l'option 1 pour l'installation complete
echo 4. Vérifiez qu'aucune erreur d'encodage n'apparaît
echo.
echo Les scripts doivent fonctionner sans erreurs comme:
echo - 'ho' n'est pas reconnu en tant que commande interne
echo - 'nstallation' n'est pas reconnu en tant que commande interne
echo.
echo Appuyez sur une touche pour continuer...
pause >nul 