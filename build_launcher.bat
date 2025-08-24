@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:menu
cls
echo.
echo ========================================
echo    🔨 LANCEUR DE BUILD MATELAS APP
echo ========================================
echo.
echo 📁 Nouvelle structure organisée
echo.
echo Options disponibles :
echo 1. 🚀 Lancer l'application
echo 2. 🔨 Build complet (Windows)
echo 3. 🍎 Build Mac
echo 4. 🧪 Tests
echo 5. 🔧 Administration
echo 6. 📚 Documentation
echo 7. 🔍 Diagnostic PyQt6
echo 8. ❌ Quitter
echo.
set /p choice="Choisissez une option (1-8) : "

if "%choice%"=="1" (
    call lancer_app_windows.bat
    goto :menu
) else if "%choice%"=="2" (
    cd build_scripts\windows
    call build_launcher.bat
    cd ..\..
    goto :menu
) else if "%choice%"=="3" (
    cd build_scripts\macos
    python3 build_mac_complet.py
    cd ..\..
    goto :menu
) else if "%choice%"=="4" (
    cd utilities\tests
    python3 test_eula_inclusion.py
    cd ..\..
    goto :menu
) else if "%choice%"=="5" (
    cd utilities\admin
    python3 admin_builder_gui.py
    cd ..\..
    goto :menu
) else if "%choice%"=="6" (
    start docs\build
    goto :menu
) else if "%choice%"=="7" (
    call diagnostic_pyqt6_windows.bat
    goto :menu
) else if "%choice%"=="8" (
    echo Au revoir !
    exit /b 0
) else (
    echo Choix invalide
    pause
    goto :menu
)
