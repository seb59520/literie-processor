@echo off
echo ========================================
echo    DIAGNOSTIC COMPLET - EXCEL + API
echo ========================================
echo.

echo 1. Test de l'API (cause principale)...
echo ----------------------------------------
python test_api_connection.py

echo.
echo 2. Test des composants Excel...
echo ----------------------------------------  
python test_excel_generation.py

echo.
echo ========================================
echo RÉSUMÉ DU PROBLÈME
echo ========================================
echo.
echo CAUSE PRINCIPALE: Erreur 401 OpenRouter
echo - L'API ne fonctionne pas
echo - Donc les PDFs ne sont pas traités  
echo - Donc pas de données pour l'Excel
echo - Donc pas de fichier Excel généré
echo.
echo SOLUTION:
echo 1. Configurez d'abord votre clé API OpenRouter
echo 2. Testez l'API avec Test_API.bat
echo 3. Une fois l'API fonctionnelle, relancez l'application
echo 4. Traitez vos PDFs - l'Excel sera généré automatiquement
echo.
pause