@echo off
echo ========================================
echo    TEST DE CONNEXION API
echo ========================================
echo.

echo Test de la configuration API...
python test_api_connection.py

echo.
echo Si vous avez une erreur 401:
echo 1. Verifiez que votre cle API est correcte
echo 2. Verifiez que votre provider LLM est le bon
echo 3. Verifiez que votre cle n'a pas expire
echo 4. Verifiez les permissions de votre cle
echo.
pause