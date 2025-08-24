@echo off
chcp 65001 >nul
echo ========================================
echo    INSTALLATION CERTIFICAT AUTO-SIGNÉ
echo    MatelasApp - SCINNOVA
echo ========================================
echo.

REM Vérifier que le certificat existe
if not exist "certificats\MatelasApp.cer" (
    echo ❌ Certificat non trouvé: certificats\MatelasApp.cer
    echo.
    echo Ce script doit être exécuté depuis le dossier de l'application
    echo ou le certificat doit être copié dans le dossier 'certificats'
    echo.
    pause
    exit /b 1
)

echo ✅ Certificat trouvé: certificats\MatelasApp.cer
echo.

echo 🔐 Installation du certificat dans le magasin de certificats Windows...
echo.

REM Installer le certificat dans le magasin racine
certmgr.exe -add -c "certificats\MatelasApp.cer" -s -r localMachine root

if %errorlevel% equ 0 (
    echo.
    echo ✅ Certificat installé avec succès!
    echo.
    echo L'application MatelasApp peut maintenant être exécutée
    echo sans alertes de sécurité Windows.
    echo.
    echo 📋 Informations:
    echo   - Certificat: SCINNOVA MatelasApp
    echo   - Émetteur: SCINNOVA MatelasApp CA
    echo   - Type: Auto-signé
    echo.
    echo 🔍 Pour vérifier l'installation:
    echo   certmgr.msc
    echo   (Magasin de certificats > Autorités de certification racines de confiance)
) else (
    echo.
    echo ❌ Erreur lors de l'installation du certificat
    echo.
    echo Essayez d'exécuter ce script en tant qu'administrateur:
    echo   Clic droit > "Exécuter en tant qu'administrateur"
    echo.
    echo Ou installez manuellement:
    echo   1. Double-clic sur certificats\MatelasApp.cer
    echo   2. Cliquer sur "Installer le certificat"
    echo   3. Choisir "Magasin de certificats local"
    echo   4. Sélectionner "Autorités de certification racines de confiance"
)

echo.
pause 