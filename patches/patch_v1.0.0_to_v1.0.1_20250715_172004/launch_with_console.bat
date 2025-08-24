@echo off
echo ========================================
echo    Lancement Application Matelas
echo    (Mode console pour debug)
echo ========================================
echo.

if exist "dist\MatelasApp\MatelasApp.exe" (
    echo Lancement de l'application...
    echo.
    echo Si l'application ne s'affiche pas, regardez les messages d'erreur ci-dessous
    echo.
    cd dist\MatelasApp
    MatelasApp.exe
) else (
    echo ERREUR: Executable non trouve
    echo Lancement avec Python direct...
    python run_gui.py
)

echo.
echo Application fermee.
pause 