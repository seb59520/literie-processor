@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:menu
cls
echo.
echo ========================================
echo    LANCEUR DE BUILD MATELASAPP
echo ========================================
echo.
echo Nouvelle structure organisee
echo.
echo Options disponibles:
echo 1. Lancer l'application
echo 2. Build complet (Windows)
echo 3. Build Mac
echo 4. Tests
echo 5. Administration
echo 6. Documentation
echo 7. Diagnostic PyQt6
echo 8. Quitter
echo.
set /p choice="Choisissez une option (1-8): "

if "%choice%"=="1" goto lancer_app
if "%choice%"=="2" goto build_windows
if "%choice%"=="3" goto build_mac
if "%choice%"=="4" goto tests
if "%choice%"=="5" goto admin
if "%choice%"=="6" goto docs
if "%choice%"=="7" goto diagnostic
if "%choice%"=="8" goto quitter

echo Option invalide. Appuyez sur une touche...
pause
goto menu

:lancer_app
echo.
echo Lancement de l'application...
call lancer_app_windows_fixe.bat
goto menu

:build_windows
echo.
echo Build Windows...
if exist "build_scripts\windows" (
    cd build_scripts\windows
    call build_launcher.bat
    cd ..\..
) else (
    echo Dossier build_scripts\windows non trouve
    pause
)
goto menu

:build_mac
echo.
echo Build Mac...
if exist "build_scripts\macos" (
    cd build_scripts\macos
    python3 build_mac_complet.py
    cd ..\..
) else (
    echo Dossier build_scripts\macos non trouve
    pause
)
goto menu

:tests
echo.
echo Tests...
if exist "utilities\tests" (
    cd utilities\tests
    python3 test_eula_inclusion.py
    cd ..\..
) else (
    echo Dossier utilities\tests non trouve
    pause
)
goto menu

:admin
echo.
echo Administration...
if exist "utilities\admin" (
    cd utilities\admin
    python3 admin_builder_gui.py
    cd ..\..
) else (
    echo Dossier utilities\admin non trouve
    pause
)
goto menu

:docs
echo.
echo Ouverture de la documentation...
if exist "docs\build" (
    start docs\build
) else (
    echo Dossier docs\build non trouve
    pause
)
goto menu

:diagnostic
echo.
echo Diagnostic PyQt6...
call diagnostic_pyqt6_windows_fixe.bat
goto menu

:quitter
echo.
echo Au revoir!
exit /b 0 