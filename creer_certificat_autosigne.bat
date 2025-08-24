@echo off
chcp 65001 >nul
echo ========================================
echo    CRÉATION CERTIFICAT AUTO-SIGNÉ
echo    ET SIGNATURE APPLICATION
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

REM Vérifier que makecert est disponible
makecert >nul 2>&1
if errorlevel 1 (
    echo ❌ makecert non trouvé
    echo.
    echo Installez Windows SDK ou Visual Studio Build Tools
    echo Téléchargement: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
    echo.
    pause
    exit /b 1
)

echo ✅ makecert disponible
echo.

REM Vérifier que signtool est disponible
signtool >nul 2>&1
if errorlevel 1 (
    echo ❌ signtool non trouvé
    echo.
    echo Installez Windows SDK ou Visual Studio Build Tools
    echo.
    pause
    exit /b 1
)

echo ✅ signtool disponible
echo.

REM Créer le dossier pour les certificats
if not exist "certificats" mkdir certificats
cd certificats

echo 🔐 Création du certificat auto-signé...
echo.

REM Créer l'autorité de certification
echo 1. Création de l'autorité de certification...
makecert -r -pe -n "CN=SCINNOVA MatelasApp CA" -ss CA -sr CurrentUser -a sha256 -cy end -sky signature -sv CA.pvk CA.cer
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de la création de l'autorité de certification
    cd ..
    pause
    exit /b 1
)
echo ✅ Autorité de certification créée

REM Créer le certificat de signature
echo 2. Création du certificat de signature...
makecert -pe -n "CN=SCINNOVA MatelasApp" -ss MY -a sha256 -cy end -sky signature -ic CA.cer -iv CA.pvk -sv MatelasApp.pvk MatelasApp.cer
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de la création du certificat
    cd ..
    pause
    exit /b 1
)
echo ✅ Certificat de signature créé

REM Convertir en PFX
echo 3. Conversion en format PFX...
pvk2pfx -pvk MatelasApp.pvk -spc MatelasApp.cer -pfx MatelasApp.pfx
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de la conversion en PFX
    cd ..
    pause
    exit /b 1
)
echo ✅ Certificat PFX créé

cd ..

echo.
echo ✅ Certificat auto-signé créé avec succès!
echo.
echo 📁 Fichiers créés dans le dossier 'certificats':
echo   - CA.cer (Autorité de certification)
echo   - MatelasApp.cer (Certificat public)
echo   - MatelasApp.pfx (Certificat privé)
echo.

REM Signer l'exécutable
echo 🔐 Signature de l'exécutable...
echo.

signtool sign /f "certificats\MatelasApp.pfx" /t http://timestamp.digicert.com /v "dist\MatelasApp.exe"

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
    echo 📋 Pour installer le certificat sur d'autres machines:
    echo   certmgr.exe -add -c "certificats\MatelasApp.cer" -s -r localMachine root
    echo.
    echo 📁 Ou utilisez le script: installer_certificat.bat
) else (
    echo.
    echo ❌ Erreur lors de la signature
    echo.
    echo Vérifiez:
    echo   - La connexion internet (pour l'horodatage)
    echo   - Les permissions d'écriture
)

echo.
pause 