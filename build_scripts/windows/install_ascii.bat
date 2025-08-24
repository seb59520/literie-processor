@echo off
chcp 65001 >nul

echo ========================================
echo    INSTALLATION COMPLETE MATELASAPP
echo ========================================
echo.

REM Aller dans le dossier racine
cd /d "%~dp0..\.."
echo Dossier: %CD%
echo.

REM Verifier Python
echo [1/5] Verification de Python...
python --version
if errorlevel 1 (
    echo ERREUR: Python non trouve
    echo    Installez Python depuis python.org
    echo    Version recommandee: Python 3.8 ou plus recent
    pause
    exit /b 1
)
echo Python trouve
echo.

REM Installer les dependances
echo [2/5] Installation des dependances...
echo Installation des packages requis...

REM Verifier si requirements_gui.txt existe
if exist "requirements_gui.txt" (
    echo    Installation depuis requirements_gui.txt...
    pip install -r requirements_gui.txt
    if errorlevel 1 (
        echo ERREUR: Echec installation depuis requirements_gui.txt
        echo    Installation des packages individuels...
        pip install PyQt6 openpyxl requests
        if errorlevel 1 (
            echo ERREUR: Echec installation packages individuels
            pause
            exit /b 1
        )
    )
) else (
    echo    Installation des packages individuels...
    pip install PyQt6 openpyxl requests
    if errorlevel 1 (
        echo ERREUR: Echec installation packages
        pause
        exit /b 1
    )
)

echo Installation de PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERREUR: Echec installation PyInstaller
    pause
    exit /b 1
)
echo Dependances installees
echo.

REM Verifier les ressources
echo [3/5] Verification des ressources...
if not exist "app_gui.py" (
    echo ERREUR: app_gui.py non trouve
    pause
    exit /b 1
)
if not exist "backend\" (
    echo ERREUR: Dossier backend non trouve
    pause
    exit /b 1
)
if not exist "config\" (
    echo ERREUR: Dossier config non trouve
    pause
    exit /b 1
)
if not exist "assets\" (
    echo ERREUR: Dossier assets non trouve
    pause
    exit /b 1
)
echo Ressources trouvees
echo.

REM Compiler l'application
echo [4/5] Compilation de l'application...
echo Lancement de la compilation...
echo    Cela peut prendre plusieurs minutes...
echo.

REM Executer le script de compilation Python
python build_scripts\windows\build_complet.py
if errorlevel 1 (
    echo ERREUR: Echec compilation
    pause
    exit /b 1
)
echo Compilation terminee
echo.

REM Verifier le resultat
echo [5/5] Verification du resultat...
if exist "dist\MatelasApp.exe" (
    echo Executable cree: dist\MatelasApp.exe
    echo.
    echo ========================================
    echo    INSTALLATION REUSSIE!
    echo ========================================
    echo.
    echo L'application a ete compilee avec succes!
    echo.
    echo Fichier cree: dist\MatelasApp.exe
    echo.
    echo Pour lancer l'application:
    echo    1. Double-cliquez sur dist\MatelasApp.exe
    echo    2. Ou utilisez le script de lancement
    echo.
    echo Voulez-vous lancer l'application maintenant? (o/n)
    set /p launch_choice="Votre choix: "
    if /i "%launch_choice%"=="o" (
        echo Lancement de l'application...
        start "" "dist\MatelasApp.exe"
        echo Application lancee!
    ) else if /i "%launch_choice%"=="oui" (
        echo Lancement de l'application...
        start "" "dist\MatelasApp.exe"
        echo Application lancee!
    )
    echo.
) else (
    echo ERREUR: Executable non trouve
    echo    Verifiez les erreurs ci-dessus
    pause
    exit /b 1
)

echo Informations importantes:
echo    - L'application est autonome (pas besoin de Python)
echo    - Tous les fichiers de configuration sont inclus
echo    - Compatible Windows 10/11
echo    - Taille approximative: 50-100 MB
echo.
echo Installation terminee avec succes!
echo.
pause 