@echo off
chcp 65001 >nul
echo ========================================
echo    SIGNATURE APPLICATION WINDOWS
echo    (Certificat Commercial)
echo ========================================
echo.

REM Vérifier que l'exécutable existe
if not exist "dist\MatelasApp.exe" (
    echo ❌ Exécutable non trouvé: dist\MatelasApp.exe
    echo.
    echo Compilez d'abord l'application avec:
    echo   python build_universal.py
    echo   ou
    echo   build_simple.bat
    echo.
    pause
    exit /b 1
)

echo ✅ Exécutable trouvé: dist\MatelasApp.exe
echo.

REM Vérifier que signtool est disponible
signtool >nul 2>&1
if errorlevel 1 (
    echo ❌ signtool non trouvé
    echo.
    echo Installez Windows SDK ou Visual Studio Build Tools
    echo Téléchargement: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
    echo.
    pause
    exit /b 1
)

echo ✅ signtool disponible
echo.

REM Demander les informations du certificat
echo 🔐 Informations du certificat:
echo.
set /p CERT_FILE="Chemin vers le certificat (.pfx): "
set /p CERT_PASSWORD="Mot de passe du certificat: "

REM Vérifier que le fichier certificat existe
if not exist "%CERT_FILE%" (
    echo ❌ Fichier certificat non trouvé: %CERT_FILE%
    pause
    exit /b 1
)

echo.
echo 🔐 Signature en cours...
echo.

REM Signer l'exécutable avec horodatage
signtool sign /f "%CERT_FILE%" /p "%CERT_PASSWORD%" /t http://timestamp.digicert.com /v "dist\MatelasApp.exe"

if %errorlevel% equ 0 (
    echo.
    echo ✅ Signature réussie!
    echo.
    echo L'application signée se trouve dans: dist\MatelasApp.exe
    echo.
    echo 🔍 Vérification de la signature:
    echo.
    signtool verify /pa "dist\MatelasApp.exe"
    echo.
    echo 📋 Informations de signature:
    echo.
    signtool verify /v /pa "dist\MatelasApp.exe"
) else (
    echo.
    echo ❌ Erreur lors de la signature
    echo.
    echo Vérifiez:
    echo   - Le chemin du certificat
    echo   - Le mot de passe
    echo   - La validité du certificat
    echo   - La connexion internet (pour l'horodatage)
)

echo.
pause 