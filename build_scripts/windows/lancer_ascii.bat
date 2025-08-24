@echo off
chcp 65001 >nul

echo ========================================
echo    LANCEMENT MATELASAPP
echo ========================================
echo.

REM Aller dans le dossier racine
cd /d "%~dp0..\.."

REM Verifier si l'executable existe
if exist "dist\MatelasApp.exe" (
    echo Lancement de MatelasApp...
    echo.
    start "" "dist\MatelasApp.exe"
    echo Application lancee!
    echo.
    echo L'application devrait s'ouvrir dans quelques secondes
    echo.
) else (
    echo ERREUR: Executable non trouve
    echo.
    echo Solutions:
    echo    1. Lancez d'abord l'installation: install_ascii.bat
    echo    2. Verifiez que la compilation s'est bien passee
    echo    3. Verifiez que le fichier dist\MatelasApp.exe existe
    echo.
    echo Voulez-vous lancer l'installation maintenant? (o/n)
    set /p install_choice="Votre choix: "
    if /i "%install_choice%"=="o" (
        echo Lancement de l'installation...
        call "build_scripts\windows\install_ascii.bat"
    ) else if /i "%install_choice%"=="oui" (
        echo Lancement de l'installation...
        call "build_scripts\windows\install_ascii.bat"
    )
)

pause 