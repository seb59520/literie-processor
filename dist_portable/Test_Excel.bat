@echo off
echo ========================================
echo    TEST DE GÉNÉRATION EXCEL
echo ========================================
echo.

echo Diagnostic de la génération Excel...
python test_excel_generation.py

echo.
echo Si aucun fichier Excel n'est généré:
echo 1. Vérifiez d'abord votre API (Test_API.bat)
echo 2. Vérifiez que des PDFs ont été traités avec succès
echo 3. Vérifiez les permissions du dossier de sortie
echo 4. Consultez les logs d'erreur détaillés
echo.
pause