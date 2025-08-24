@echo off
chcp 65001 >nul
title Generation Documentation Complete - MatelasApp Westelynck

echo ========================================
echo    GENERATION DOCUMENTATION COMPLETE
echo ========================================
echo.
echo MatelasApp Westelynck - Documentation complete
echo.
echo Ce script genere la documentation complete
echo incluant toutes les informations sur :
echo - Systeme de dates et semaines
echo - Systeme d'alertes en temps reel
echo - Modules de creation et construction
echo - Scripts de build manuels
echo.
echo ========================================
echo.

REM Verification de Python
echo [1/4] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python non trouve
    echo Veuillez installer Python 3.8+ et reessayer
    pause
    exit /b 1
)
echo OK: Python trouve

REM Verification de reportlab
echo [2/4] Verification de reportlab...
python -c "import reportlab" >nul 2>&1
if errorlevel 1 (
    echo Installation de reportlab...
    pip install reportlab
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer reportlab
        pause
        exit /b 1
    )
)
echo OK: reportlab disponible

REM Generation de la documentation
echo [3/4] Generation de la documentation...
python create_documentation_complete_pdf.py
if errorlevel 1 (
    echo ERREUR: Echec de la generation de la documentation
    pause
    exit /b 1
)

REM Verification du fichier genere
echo [4/4] Verification du fichier genere...
if exist "Documentation_MatelasApp_Westelynck_Complete.pdf" (
    echo OK: Documentation generee avec succes
    echo.
    echo ========================================
    echo    DOCUMENTATION GENERE AVEC SUCCES
    echo ========================================
    echo.
    echo Fichier cree: Documentation_MatelasApp_Westelynck_Complete.pdf
    echo.
    echo Contenu de la documentation:
    echo - Vue d'ensemble de MatelasApp
    echo - Systeme de dates et semaines
    echo - Systeme d'alertes en temps reel
    echo - Modules de creation et construction
    echo - Scripts de build manuels (ASCII)
    echo - Installation et configuration
    echo - Utilisation de l'application
    echo - Depannage et maintenance
    echo - Support et contact
    echo.
    echo Voulez-vous ouvrir le fichier PDF? (O/N)
    set /p open_pdf="Votre choix: "
    if /i "%open_pdf%"=="O" (
        start "" "Documentation_MatelasApp_Westelynck_Complete.pdf"
    )
) else (
    echo ERREUR: Fichier PDF non trouve
    pause
    exit /b 1
)

echo.
echo ========================================
echo    GENERATION TERMINEE
echo ========================================
echo.
echo La documentation complete a ete generee
echo avec toutes les informations mises a jour.
echo.
pause 