@echo off
echo ========================================
echo    TEST DE REDIMENSIONNEMENT 
echo ========================================
echo.

echo Application du fix de redimensionnement...
python quick_resize_fix.py

echo.
echo Test de l'interface...
echo Si la fenetre ne se redimensionne toujours pas:
echo 1. Utilisez Alt+Espace puis Agrandir
echo 2. Double-cliquez sur la barre de titre
echo 3. Faites glisser les bords de la fenetre

echo.
pause