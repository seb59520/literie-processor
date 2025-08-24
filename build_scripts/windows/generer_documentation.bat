@echo off
echo ========================================
echo    Generation Documentation PDF
echo ========================================
echo.

echo Installation des dependances...
pip install reportlab

echo.
echo Generation de la documentation PDF...
python create_documentation_pdf.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    Documentation generee avec succes!
    echo ========================================
    echo.
    echo Le fichier PDF se trouve dans:
    echo   Documentation_MatelasApp_Westelynck.pdf
    echo.
    echo Pour ouvrir le PDF:
    echo   start Documentation_MatelasApp_Westelynck.pdf
    echo.
) else (
    echo.
    echo ========================================
    echo    Erreur lors de la generation
    echo ========================================
    echo.
    echo Verifiez que:
    echo   1. Python est installe et dans le PATH
    echo   2. Le logo Westelynck est present dans assets/
    echo   3. Tous les fichiers du projet sont presents
    echo.
)

pause 